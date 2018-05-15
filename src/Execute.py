#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
import argcomplete, argparse, inspect, Library

parser = argparse.ArgumentParser(description='description')
subparsers = parser.add_subparsers(dest="function_called")

# Tuples: (function_name, function_pointer)
callable_functions = inspect.getmembers(Library, lambda function: inspect.isfunction(function) and not '__' in function.__name__)

for (function_name, function_pointer) in callable_functions:
    arg_spec = inspect.getargspec(function_pointer)
    # First element contains the arguments
    # TODO: Add default artguments, it doesn't support them yet
    args = arg_spec[0]

    parser_option = subparsers.add_parser(function_name)

    for arg in args:
        # Don't know why, but it needs an "--"
        parser_option.add_argument("--" + arg)

argcomplete.autocomplete(parser)
args_namespace = parser.parse_args()
args = vars(args_namespace).values()

# The function name is the last element, then we take it out from the args.
function_to_call = getattr(Library, args.pop())
function_to_call(*args)
