import subprocess
from datetime import datetime

def count_syslog_levels():    
    # Commands to count each log level using grep
    commands = {
        'INFO': "grep -i 'info' /var/log/syslog | wc -l",
        'WARN': "grep -iE '(warn|warning)' /var/log/syslog | wc -l", 
        'ERROR': "grep -iE '(error|err)' /var/log/syslog | wc -l"
    }
    
    results = {}
    
    for level, command in commands.items():
        try:
            # Run the shell command
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                count = int(result.stdout.strip()) if result.stdout.strip().isdigit() else 0
                results[level] = count
            else:
                results[level] = 0
        except Exception:
            results[level] = 0
    
    return results

def main():
    """Collect data and output CSV format to stdout"""
    
    # Get current timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Count log levels
    counts = count_syslog_levels()
    
    # Output CSV format to stdout (client will capture this)
    print("timestamp,INFO,WARN,ERROR")
    print(f"{timestamp},{counts['INFO']},{counts['WARN']},{counts['ERROR']}")

if __name__ == "__main__":
    main()