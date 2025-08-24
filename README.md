# Syslog Monitor

A Python application that monitors system log levels (INFO, WARN, ERROR) on a remote Ubuntu server via SSH and saves the data locally as CSV.

## Project Structure

```
├── client.py    # Local client that connects to remote server
├── server.py    # Remote script that analyzes syslog
└── README.md    # Documentation
```

## Prerequisites

### Local Machine Requirements

- Python 3.x
- Required Python packages:
  ```bash
  pip install paramiko pandas
  ```

### Remote Server Requirements

- Ubuntu/Linux server with SSH access
- Python 3.x installed
- SSH key-based authentication set up

## Setup Instructions

### 1. Configure SSH Access

1. Generate an SSH key pair if you don't have one:

   ```bash
   ssh-keygen -t rsa -b 2048 -f mykey
   ```

2. Copy your public key to the remote server:
   ```bash
   ssh-copy-id -i mykey.pub username@your-server-ip
   ```

### 2. Deploy Server Script

Copy `server.py` to your remote Ubuntu server:

```bash
scp -i mykey server.py username@your-server-ip:/home/username/
```

### 3. Configure Client Settings

Edit the following variables in `client.py` to match your setup:

```python
pem_file_path = "/path/to/your/mykey"      # Path to your private key
host = "your-server-ip"                    # Your server's IP address
username = "your-username"                 # Your SSH username
server_script_path = "/home/your-username/server.py"  # Path to server.py on remote machine
```

## Running the Application

1. **Start the monitoring**:

   ```bash
   python client.py
   ```

2. **Expected output**:
   ```
   Starting syslog analysis...
   Connecting to server...
   Connected to your-server-ip
   Running server.py on remote machine...
   Received data from server:
   timestamp,INFO,WARN,ERROR
   2024-01-15 10:30:45,245,12,3
   ✅ Data saved to syslog_data.csv
   New data:
     Timestamp: 2024-01-15 10:30:45
     INFO: 245
     WARN: 12
     ERROR: 3
   SSH connection closed
   Done!
   ```

## Output

The application creates/appends to `syslog_data.csv` in the same directory with the following format:

```csv
timestamp,INFO,WARN,ERROR
2024-01-15 10:30:45,245,12,3
2024-01-15 10:35:50,247,12,3
```

## How It Works

1. **Client** (`client.py`) connects to the remote server via SSH
2. **Server script** (`server.py`) runs remotely and analyzes `/var/log/syslog`:
   - Counts INFO level messages
   - Counts WARN/WARNING level messages
   - Counts ERROR/ERR level messages
3. **Results** are sent back as CSV format and saved locally

## Troubleshooting

### SSH Connection Issues

- Verify your private key path and permissions (`chmod 600 mykey`)
- Ensure your public key is in the server's `~/.ssh/authorized_keys`
- Check if the server IP and username are correct

### Permission Issues on Server

If you get permission errors accessing `/var/log/syslog`:

```bash
# Run with sudo (modify server.py if needed)
sudo python3 server.py
```

### Python Dependencies

If you encounter import errors:

```bash
pip install --upgrade paramiko pandas
```


