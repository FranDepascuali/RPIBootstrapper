#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import re

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_statement(message):
    print Colors.HEADER + "→ " + message + Colors.ENDC

def print_info(message):
    print Colors.OKBLUE + "Info: "
    pretty_message = '\t'.join(('\n' + message.lstrip()).splitlines(True))
    new_lines = pretty_message.count("\n")
    # if new_lines > 1:
        # pretty_message = pretty_message[pretty_message.find('\n') + 1 : pretty_message.rfind('\n')]
    pretty_message = re.sub('\n', '', pretty_message, 1)
    print pretty_message + Colors.ENDC

def print_success(message):
    print Colors.OKGREEN + "✔ " + message + Colors.ENDC
    print ""

def print_error(message):
    print Colors.FAIL + "Failed: " + message + Colors.ENDC
    raise SystemExit

def request_input(message):
    return raw_input(Colors.HEADER + "→ " + message + Colors.ENDC)

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
