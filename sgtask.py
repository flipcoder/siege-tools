#!/usr/bin/env python
"""
Siege-Tools SiegeTask (\"sgtask\")
CLI Task Planning
Version 0.0.1
Copyright (c) 2012 Grady O'Connell
"""

import os, sys
from common import Args
from common import Settings
from xml.dom import minidom

app_valid_anywhere = ["help", "?"]
Args.app_valid_options = ["version"]
Args.app_valid_keys = []
Args.app_valid_commands = ["list", "add", "remove", "delete", "done", "push", "pop", "change"]
Args.app_command_alias = {
    "ls":"list",
    "a":"add",
    "rm":"remove",
    "del":"delete",
    "do":"done",
    "x":"done",
    "c":"change",
    "h":"head",
    "t":"tail",
    "p":"push",
    "P":"pop"
}

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
    Args.process()
    if Args.option("version"):
        splash()
        return
    if Args.anywhere("help") or Args.anywhere("?"):
        help()
        return
    #tasks_file = open("sgtasks.xml","rw")
    #xml = minidom.parse(tasks_file)
    #idx = 0
    #for e in xml.childNodes[0].childNodes:
    #    if e.localName and e.localName.lower() == "task":
    #        try:
    #            task_desc = e.childNodes[0].data
    #            if task_desc:
    #                print "%s + %s (10/10)" % (idx, task_desc.strip())
    #            idx += 1
    #        except:
    #            pass
    #    #print e.nodeName
    #    #print "%s%s" % (" "*(len(str(len(xml.childNodes)))+1), e.nodeValue)
    #tasks_file.close()

if __name__ == "__main__":
    main()

