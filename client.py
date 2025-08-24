import paramiko
import pandas as pd
import os
import io  # <-- YOU WERE MISSING THIS IMPORT

class SshToServer:
    def __init__(self,pem_file_path, host, username):
        self.pem_file_path = pem_file_path
        self.host = host
        self.username = username
        self.sshClient = paramiko.SSHClient()
        self.connect()

    def connect(self):
        self.sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        private_key = paramiko.RSAKey.from_private_key_file(self.pem_file_path)
        self.sshClient.connect(self.host, username=self.username, pkey=private_key)
        print(f"Connected to {self.host}")

    def run_remote_command(self, command):
        try:
            stdin, stdout, stderr = self.sshClient.exec_command(command)
            output = stdout.read().decode()
            error = stderr.read().decode()
            return [output, error]
        except Exception as e:
            print(f"An error occurred while executing the command: {e}")
            return [None, str(e)]
    
    def close(self):
        if self.sshClient:
            self.sshClient.close()
            print("SSH connection closed")

def append_to_csv(file_path, data):
    df_new = pd.DataFrame([data])
    if os.path.isfile(file_path):
        df_existing = pd.read_csv(file_path)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_combined = df_new
    df_combined.to_csv(file_path, index=False)

def main():
    pem_file_path = "C:\\Users\\omerb\\keys\\mykey.pem"    
    host = "54.211.24.236"                  
    username = "ubuntu"
    server_script_path = "/home/ubuntu/server.py"  
    local_csv_file = "syslog_data.csv"         
    
    print("Starting syslog analysis...")
    
    try:
        # 1. SSH into the server
        print("Connecting to server...")
        ssh = SshToServer(pem_file_path, host, username)
        
        # 2. Run server.py on the remote machine
        print("Running server.py on remote machine...")
        command = f"python3 {server_script_path}"
        output, error = ssh.run_remote_command(command)
        
        if error:
            print(f"Error from server: {error}")
        
        if not output:
            print("No output received from server!")
            ssh.close()
            return
        
        print("Received data from server:")
        print(output)
        
        # Parse the CSV output from server
        lines = output.strip().split('\n')
        
       
        csv_lines = []
        for line in lines:
            if 'timestamp' in line or (',' in line and len(line.split(',')) == 4):
                csv_lines.append(line)
        
        if len(csv_lines) >= 2:  
            csv_data = '\n'.join(csv_lines)
            df = pd.read_csv(io.StringIO(csv_data))
            
            data_row = df.iloc[-1].to_dict()  
            
            # 5. Save to local CSV using append_to_csv
            append_to_csv(local_csv_file, data_row)
            
            print(f"✅ Data saved to {local_csv_file}")
            print("New data:")
            print(f"  Timestamp: {data_row['timestamp']}")
            print(f"  INFO: {data_row['INFO']}")
            print(f"  WARN: {data_row['WARN']}")
            print(f"  ERROR: {data_row['ERROR']}")
            
        else:
            print("❌ Could not parse CSV data from server output")
        
        # 6. Close SSH connection
        ssh.close()
        print("Done!")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()