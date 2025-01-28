# BD1 

## ⚠️ Ethical Use Disclaimer ⚠️

**WARNING**: This tool is strictly for educational and authorized network management purposes for my project cybersecurity.

- Unauthorized access to computer systems is a criminal offense
- Use only with explicit permission
- Comply with all applicable legal and ethical standards

## Overview

BD1 is a Python-based network management utility designed for system administrators to monitor and manage network endpoints.

### Components

- **Server (`sv.py`)**: Central management interface
- **Client (`bd.py`)**: Remote connection and system interaction script

## Features

### Server Capabilities
- Multiple client connection management
- Remote command execution
- Secure file transfer
- Comprehensive system information gathering
- Remote system control operations
#### Available Commands

#### General Commands
- `help`: Show all available commands

- `list`: Display connected clients
- `select <client_id>`: Target specific client
- `exit`: Close server connection

#### File Operations
- `download <file>`: Retrieve file from client 

- `upload <file>`: Send file to client

#### System Control
- `allclients`: Broadcast command to all clients 

- `shutdown`: Remote machine shutdown
- `reboot`: Remote machine restart
- `sysinfo`: Gather system information
- `cd <path>`: Change working directory

#### Advanced Operations
- `runadmin <program>`: Execute with admin privileges

- `persist`: Add system persistence
- `selfdelete`: Remove tool traces

### Client Capabilities
#### System Interaction
- Persistent network connection
- Remote command execution
- Secure file management
- System information collection

#### Stealth Capabilities
- Antivirus evasion techniques
- Process hiding
- Self-preservation mechanisms

#### Connection Management
- Automatic reconnection
- Secure session handling
- System information transmission

#### System Control
- File upload/download
- Remote command execution
- System shutdown/reboot
- Directory navigation

#### Advanced Techniques
- Administrator command execution
- Persistence methods
- Self-deletion

#### Anti-Detection Mechanisms
- Camouflage as system processes
- Randomized evasion strategies
- Minimal system footprint

## Prerequisites

- Python 3.7+
- Required packages (see `requirements.txt`)

## Installation

1. Clone the repository
   ```bash
   git clone https://github.com/miraclegalaxys/BD1.git
   cd BD1
   ```

2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Server Startup
```bash
python sv.py
```

### Key Commands
- `help`: Display available commands

- `list`: Show connected clients
- `select <client_id>`: Target specific client

## Security Recommendations

- Use only in controlled, authorized environments
- Implement additional authentication layers
- Regularly update and patch the tool
- Monitor and log all access attempts

## Contributing

Contributions are welcome. Please follow these guidelines:
- Fork the repository
- Create a feature branch
- Commit changes with clear descriptions
- Submit a pull request

Ensure all contributions:
- Maintain ethical use principles
- Follow security best practices
- Provide clear documentation

## License

- [MIT License](LICENSE)

## Disclaimer

"This tool is provided strictly for educational purposes. Any misuse or application outside the scope of this study is beyond my responsibility. Please note that any errors or inaccuracies resulting from its use are not attributable to me."

## Author

By ggalaxys_
