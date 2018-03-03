#!/usr/bin/env python

import argparse
import paramiko
import socket


DEFAULT_USER = 'admin'
DEFAULT_PASSWORD = 'password'
DEFAULT_PORT = 22
DEFAULT_TIMEOUT = 30
DEFAULT_COMMANDS = [
    'ping -w 5 -q 127.0.0.1'
]


def ssh_client(host, username, password, port, timeout, commands):
    results = []

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(hostname=host, username=username, password=password,
                       timeout=timeout, look_for_keys=False, 
                       allow_agent=False)
    except paramiko.ssh_exception.AuthenticationException: 
        return (False, 'Authentication filed.')
    except paramiko.ssh_exception.NoValidConnectionsError:
        return (False, 'Unable to connect to port {port}.'.format(port=port))
    except paramiko.ssh_exception.SSHException:
        return (False, 'No existing session.')
    except socket.timeout:
        return (False, 'Timed out.')
    except socket.gaierror: 
        return (False, 'Name or service not known')
    except EOFError:
        return (False, 'EOF error')
    except TimeoutError:
        return (False, 'Connection time out.')
    except KeyboardInterrupt:
        return (False, 'Keyboard interrupt.')

    for command in commands:
        stdin, stdout, stderr = client.exec_command(command)
        data = stdout.read().decode('utf-8') + stderr.read().decode('utf-8')
        results.append(data)

    return (True, results)


def _main(host_address, user, password, port, timeout, commands):
    results = ssh_client(host_address, user, password, port, timeout, commands)
    if results[0]:
        results = zip(commands, results[1])
        for result in results:
            print('Command: {}\nResult:'.format(result[0]))
            for line in result[1].split('\n'):
                print(line)
    else:
        print('ERROR: {}'.format(results[1]))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='SSH executor',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--user', '-U', default=DEFAULT_USER, 
                        help='User login')
    parser.add_argument('--password', '-P', default=DEFAULT_PASSWORD, 
                        help='User password')
    parser.add_argument('--port', '-p', type=int, choices=range(1, 65535),
                        metavar='{1-65535}', default=DEFAULT_PORT, 
                        help='Remote port')
    parser.add_argument('--timeout', '-t', default=DEFAULT_TIMEOUT, 
                        help='Timeout in seconds')
    parser.add_argument('host_address', help='Host name or IP address')
    parser.add_argument('commands', nargs='*', default=DEFAULT_COMMANDS,
                        help="One or many commands")
    args = parser.parse_args()

    user = args.user
    password = args.password
    host_address = args.host_address
    port = args.port
    timeout = args.timeout
    commands = args.commands

    _main(host_address, user, password, port, timeout, commands)
