#!/usr/bin/env python
"""
Siege-Tools SiegeMod (\"sgmod\")
Multi-Language Preprocessor
Version 0.0.1
Copyright (c) 2012 Grady O'Connell
"""

import os, sys
from common import Args
from common import Settings

def splash():
    print __doc__.strip()

def commands():
    print("Commands: %s" % ", ".join(Args.valid_commands))

def help():
    splash()
    print()
    commands()

def main():
    Args.valid_anywhere= ["help"]
    Args.valid_options = ["version", "verbose", "strict"]
    Args.valid_commands = []
    Args.valid_keys = []
    #Args.command_aliases = {"?":"help", "ls":"list"}
    Args.process()

if __name__ == "__main__":
    main()

