from flask import Flask, render_template, request, send_from_directory
import subprocess
import sqlite3
import xml.etree.ElementTree as ET

app = Flask(__name__, template_folder='template', static_url_path='/static')

def fun():
    command = "timeout 10s sudo netdiscover -P >> available_ips.txt"
    subprocess.run(["konsole", "-e", "bash", "-c", command])

def avail_ips():
    with open('available_ips.txt', 'r') as file:
        lines = file.readlines()

    ip_addresses = []

    for line in lines:
        parts = line.split()
        if len(parts) >= 1:
            ip = parts[0]
            ip_addresses.append(ip)

    unwanted = ['___________________________', 'IP', '-----------------------------------------------------------------------------']
    for i in ip_addresses:
        if i in unwanted:
            ip_addresses.remove(i)
    return ip_addresses

def os_scan(target):
    filename = f"os_scan_results_{target}.xml"
    command = f"nmap -O -sV -oX {filename} {target} > os_scan_results.xml"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if stderr:
        return f"Error occurred: {stderr.decode()}", None
    else:
        highest_accuracy_cpe = get_highest_accuracy_cpe(filename)
        return f"Scan completed successfully for {target}.", highest_accuracy_cpe

def get_highest_accuracy_cpe(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    highest_accuracy = 0
    highest_accuracy_cpe = None

    for osmatch in root.findall(".//osmatch"):
        accuracy = int(osmatch.get("accuracy"))
        cpe_element = osmatch.find(".//cpe")
        if cpe_element is not None and accuracy > highest_accuracy:
            highest_accuracy = accuracy
            highest_accuracy_cpe = cpe_element.text

    return highest_accuracy_cpe

def search_cves_by_cpe(cpe):
    database_file = "cpe.db"
    try:
        conn = sqlite3.connect(database_file)
        cursor = conn.cursor()

        # Execute the SQL query to select the 'cpe' field
        cursor.execute("SELECT * FROM cpe_table WHERE cpe LIKE ?", ('%' + cpe + '%',))
        cve_entries = cursor.fetchall()

        if cve_entries:
            return cve_entries
        else:
            return [("No CVEs found", "No description")]

    except sqlite3.Error as e:
        print("Error connecting to SQLite database:", e)

    finally:
        if conn:
            conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    target = request.form['target']
    xml_files = []
    result, highest_accuracy_cpe = os_scan(target)
    if "Scan completed successfully" in result:
        xml_files.append(f'os_scan_results_{target}.xml')
        cve_entries = search_cves_by_cpe(highest_accuracy_cpe)
    else:
        cve_entries = []

    return render_template('full_scan_result.html', result=result, xml_files=xml_files, cve_entries=cve_entries)

@app.route('/download/<filename>')
def download(filename):
    directory = '/home/shambhavi/Documents/flask_app/'  # Specify the directory path
    return send_from_directory(directory, filename, as_attachment=True)

@app.route('/full_scan', methods=['GET', 'POST'])
def full_scan():
    fun()
    ips = avail_ips()
    if not ips:
        return render_template('full_scan_result.html', result="No IP addresses found.")
    
    scan_results = []
    for ip in ips:
        if ip == "IP": 
            continue
        else:
            result, highest_accuracy_cpe = os_scan(ip)
            cpe = highest_accuracy_cpe
            if cpe:
                cve_entries = search_cves_by_cpe(cpe)
                scan_results.append((ip, result, highest_accuracy_cpe, cve_entries))
            else:
                scan_results.append((ip, result, highest_accuracy_cpe, []))
    
    return render_template('full_scan_result.html', scan_results=scan_results)

if __name__ == "__main__":
    app.run(debug=True)