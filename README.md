
# Network Vulnerability Scanner

This project is a web-based network vulnerability scanner built using Flask. It identifies active IP addresses in the network and performs operating system and service version detection. Additionally, it checks for known vulnerabilities (CVEs) based on the detected operating system.

## Features

- **IP Discovery**: Scans the network for active IP addresses.
- **OS and Service Detection**: Uses Nmap to detect the operating system and services running on the discovered IP addresses.
- **CVE Search**: Looks up known vulnerabilities based on the detected OS and service versions.

## Prerequisites

- Python 3.x
- Flask
- Nmap
- SQLite

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Shambhavi-03/MATRIX.git
    cd MATRIX
    ```

2. Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Ensure `nmap` and `netdiscover` are installed on your system:
    ```bash
    sudo apt-get install nmap netdiscover
    ```

5. Set up the SQLite database:
    ```bash
    sqlite3 cpe.db < schema.sql
    ```

## Usage

1. Run the Flask application:
    ```bash
    python app.py
    ```

2. Open your web browser and navigate to `http://127.0.0.1:5000`.

3. Use the web interface to:
    - Discover IP addresses in your network.
    - Perform OS and service detection on a specific IP address.
    - View known vulnerabilities based on the detected OS and service versions.

## Project Structure

- `app.py`: Main Flask application file.
- `templates/`: HTML templates for the web interface.
- `static/`: Static files (e.g., CSS, JS).
- `available_ips.txt`: Temporary file to store discovered IP addresses.
- `schema.sql`: SQL schema file to set up the SQLite database.

## Security Considerations

- **Running Commands**: The application runs system commands that require `sudo` privileges. Ensure the Flask application is properly secured and avoid exposing it to untrusted networks.
- **Database**: Keep your `cpe.db` file secure and regularly update it with the latest CVE information.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


