#!/usr/bin/env python
"""
Siege-Tools SiegeTask (\"sgtask\")
CLI Task Planning
Version 0.0.1
Copyright (c) 2012 Grady O'Connell
"""

import os, sys
#from common import Args
from common import Settings

#app_valid_anywhere = ["help", "?"]
#Args.app_valid_options = ["version","count"]
#Args.app_valid_keys = []
#Args.app_valid_commands = ["list", "add", "remove", "delete", "done", "push", "pop", "change","fold"]
#Args.app_command_alias = {
#    "ls":"list",
#    "a":"add",
#    "rm":"remove",
#    "del":"delete",
#    "do":"done",
#    "x":"done",
#    "c":"change",
#    "h":"head",
#    "t":"tail",
#    "p":"push",
#    "P":"pop",
#    "f":"fold"
#}

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

def arg(idx):
    try:
        return sys.argv[idx]
    except:
        return ""

class Counter:
    def __init__(self, value):
        self.value = value
    def get(self):
        return self.value
    def add(self, value=1):
        self.value += value
    def set(self, value):
        self.value = value

class Task(object):
    def __init__(self, text="", fn = "", parent=None):
        self.subtasks = []
        self.text = ""
        self.modified = False
        if text:
            self.text = text
        if fn:
            tasks_file = open(fn,"r+")
            tasks = tasks_file.readlines()
            self.load_file(tasks)
            tasks_file.close()
    #def add(self, task):
    #    self.subtasks += task
    def __str__(self):
        return self.to_string()
    def save(self, fn=""):
        f = open(fn, "w")
        f.write(self)
        f.close()
    def to_string(self, indent=-1, counter=None):
        s = ""
        if self.text:
            if counter:
                s += str(counter.get()) + " "
            if indent > 0:
                s += " " * (indent * 4)
            s += self.text + os.linesep
            counter.add()
            
        for task in self.subtasks:
            s += task.to_string(indent+1, counter)
        return s
    def set_text(self,t):
        self.text = t
    def load_file(self, tasks, offset=0, cur_indent=-1):
        skip = False
        for i in xrange(offset, len(tasks)):
            if not tasks[i].strip():
                continue # ignore blank lines

            indent = 0
            try:
                while tasks[i][indent] == " ":
                    indent += 1
            except:
                continue

            indent = indent / 4

            if indent == cur_indent + 1:
                self.subtasks += [Task(text=tasks[i].strip(), parent=self)]
                skip = False
            elif indent > cur_indent + 1:
                if not skip:
                    self.subtasks[-1].load_file(tasks, i, indent-1)
                skip = True
            else:
                return

    def __len__(self):
        return self.count()

    def count(self):
        count = len(self.subtasks)

        for t in self.subtasks:
            count += t.count()

        return count

    def num_subtasks(self):
        return len(self.subtasks)
    def subtask(self,i):
        try:
            return self.subtasks[i]
        except:
            pass
        return None
    def add(self, task):
        if task:
            subtasks += [task]
            return True
        return False

def do_add(tasks):
    # read until a "marker" token or end
    # marker example: "+ 1" which means to add to task numbered 1
    if len(sys.argv) <= 2:
        return False

    marker = len(sys.argv)
    for i in xrange(2,len(sys.argv)):
        if sys.argv[i] == "+":
            marker = i
    for i in xrange(2,len(sys.argv)):
        if marker:
            entry = " ".join(sys.argv[2:marker])
            try:
                if not tasks.subtask(-1).add(entry):
                    print "error1" #TODO
            except:
                print "error2" #TODO
    return True

def main():
    arg_idx = 1
    token = arg(arg_idx)

    if token == "-v" or token == "-version" or token == "--version":
        splash()
        return

    if token == "help" or token == "-h" or token == "-help" or token == "--help":
        help()
        return
    
    tasks = Task(fn="sgtasks")

    if token == "a" or token == "add":
        if not do_add(tasks):
            print "error3" # TODO
    if token == "f" or token == "fold":
        pass

    print tasks.to_string(counter=Counter(0))
    print len(tasks)

if __name__ == "__main__":
    main()

