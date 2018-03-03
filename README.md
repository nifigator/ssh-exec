# Program for executing commands on remote devices.

## Usage
    usage: ssh_exec.py [-h] [--user USER] [--password PASSWORD] [--port {1-65535}]
                       [--timeout TIMEOUT]
                       host_address [commands [commands ...]]
    
    SSH executor
    
    positional arguments:
      host_address          Host name or IP address
      commands              One or many commands (default: ['ping -w 5 -q
                            127.0.0.1'])
    
    optional arguments:
      -h, --help            show this help message and exit
      --user USER, -U USER  User login (default: admin)
      --password PASSWORD, -P PASSWORD
                            User password (default: password)
      --port {1-65535}, -p {1-65535}
                            Remote port (default: 22)
      --timeout TIMEOUT, -t TIMEOUT
                            Timeout in seconds (default: 30)
    

The program was tested in Python version 2.7.12 add 3.5.2 in Linux Ubuntu 16.04.
