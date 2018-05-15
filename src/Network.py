import paramiko
import os
from IOManager import *

def ssh_forget_host(host):
    directive = "Forgetting ssh host's {} key".format(host)
    command = "ssh-keygen -R {}".format(host)
    success = "ssh host forgotten"

    __call__(directive, command, success)

def print_hosts_in_network(ip, mask):
    directive = "Listing hosts in {}/{}".format(ip, mask)
    command = "nmap -n -sP {}/{}".format(ip, mask)
    success = "Hosts listed"

    __call__(directive, command, success)

project_directory = os.path.dirname(os.path.realpath(__file__))
known_hosts_path = os.path.join(project_directory, "known_hosts")

def establish_ssh_connection(host, username, password):
    client = paramiko.SSHClient()

    client.load_host_keys(os.path.join(os.path.dirname(__file__), known_hosts_path))
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    client.connect(host, username = username, password = password)

    stdin, stdout, stderr = client.exec_command('ls')
    for line in stdout:
        print('... ' + line.strip('\n'))
    client.close()

def __call__(directive, command, success_message, requires_privileges = False):
    if not directive == "":
        print_statement(directive)
    try:
        if requires_privileges:
            # We need tu run it with shell true if in sudo.
            output = subprocess.check_output("sudo {}".format(command), shell = True, stderr=subprocess.STDOUT)
        else:
            output = subprocess.check_output(command, shell = True, stderr = subprocess.STDOUT)
        print_info(output)
        if not success_message == "":
            print_success(success_message)
    except subprocess.CalledProcessError as error:
        print_error(error.output)
        pass # handle errors in the called executable
    except OSError as error:
        print_error(error.strerror)
        pass # executable not found
