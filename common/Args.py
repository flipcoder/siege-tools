#!/usr/bin/env python
import sys, os

# prog option
# prog --command
# prog -a
# prog --mapkey=mapvalue

options = []
commands = []
arg_map = {}

valid_options = []
valid_keys = []
valid_commands = []
valid_anywhere = []
command_aliases = {}
filenames = []
allow_strings = False

def option(s):
    if s in options:
        return True
    return False

def value(s):
    if s in arg_map:
        return arg_map[s]
    return None

def command(s):
    if s in commands:
        return True
    return False

def anywhere(s):
    if s in commands or s in options:
        return True
    return False

def process():
    global valid_commands
    global valid_options
    global valid_keys
    global filenames
    valid_commands = valid_anywhere + valid_commands
    valid_options = valid_anywhere + valid_options

    for arg in sys.argv[1:]:
        #arg_case = arg
        #arg = arg.lower()
        if arg.startswith("--"):
            if '=' in arg:
                idx = arg.find("=")
                key = arg[2:idx]
                try:
                    value = arg[idx+1:]
                except:
                    print "No key specified for parameter \'%s\'" % arg
                    exit(1)
                    #break
                    
                if key not in valid_keys:
                    print "Invalid key \'%s\'" % key
                    exit(1)

                if key not in arg_map:
                    arg_map[key] = value
            else:
                entry = arg[2:]
                if entry not in valid_options:
                    print "Invalid parameter \'%s\'" % entry
                    exit(1)
                elif entry not in options:
                    options.append(entry)

        elif arg.startswith("-"):
        #    arg = arg[1:]
        #    if arg in valid_options:
        #        options.append(arg)
        #    else:

            letters = arg[1:]
            if (len(letters) == 0):
                print "Invalid paramter \'%s\'" % arg
                exit(1)

            # if user passes something like -version, allow it as a normal parameter,
            # instead of each letter -v -e -r -s... etc.
            #if letters in valid_anywhere:
            #    options.append(letters)
            #    continue
            if letters in valid_options:
                options.append(letters)
                continue

            # otherwise look through each letter for each parameter meaning
            for ch in letters:
                matched_arg = False
                num_matches = 0

                for name in valid_options:
                    if ch == name[:1]:
                        if num_matches == 0:
                            matched_arg = True
                            if name not in options:
                                options.append(name)
                            break
                    elif ch == name[:1].upper():
                        # uses secondary match if the letter is capitalized
                        # example: -v matches version, -V matches verbose
                        if num_matches > 0: 
                            matched_arg = True
                            if name not in options:
                                options.append(name)
                            break
                        num_matches += 1

                if not matched_arg:
                    print "Invalid parameter \'-%s\'" % ch
                    exit(1)

        else:
            filenames += [arg_case]
            # no prefix dashes (-) on argument means its a command or  filename

            # TODO: add back in commands
            #if arg in valid_commands:
            #    commands.append(arg);
            #elif arg in command_aliases and command_aliases[arg] in valid_commands:
            #    commands.append(command_aliases[arg])
            #else:
            #    print "Invalid command \'%s\'" % arg
            #    exit(1)

