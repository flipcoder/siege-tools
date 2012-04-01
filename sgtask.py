#!/usr/bin/env python
"""Siege-Tools SiegeTask (\"sgtask\")
CLI Task Planning
Version 0.0.1
Copyright (c) 2012 Grady O'Connell
"""

import os, sys
from common import Args
from common import Settings

app_valid_anywhere = ["help", "?"]
Args.app_valid_options = app_valid_anywhere + ["version"]
Args.app_valid_keys = []
Args.app_valid_commands = app_valid_anywhere + ["list", "add", "remove", "delete", "done", "push", "pop"]
Args.app_command_alias = {
    "ls":"list",
    "a":"add",
    "rm":"remove",
    "del":"delete",
    "do":"done",
    "x":"done"
}
Args.allow_strings = True

class Task:
    def __init__(self, title):
        self.title = title
    def __str__(self):
        return self.title

def splash():
    print __doc__

def commands():
    print("Commands: %s" % ", ".join(Args.app_valid_commands))

def help():
    splash()
    print("")
    commands()

def main():
    if Args.option("version"):
        splash()
        return
    if Args.anywhere("help") or Args.anywhere("?"):
        help()
        return

if __name__ == "__main__":
    main()

