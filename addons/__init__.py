#!/usr/bin/env python
import sys,os, imp

base = {}

def process_path(path):
    global base
    if not os.path.exists(path):
        return
    if not os.path.abspath(path) in sys.path:
        sys.path.append(path)

    for fn in os.listdir(path):
        if fn.lower().endswith(".py") and not fn.lower() == "__init__.py":
            name = fn[:-3]
            base[name] = __import__(name, globals(), locals(), [], -1)
            #if hasattr(base[fn],"category"): # TODO addon categories
        elif os.path.isdir(os.path.join(path,fn)):
            base[fn] = __import__(fn, globals(), locals(), [], -1)

def process():
    process_path(os.path.dirname(os.path.realpath(__file__)))
    process_path(os.path.join(os.environ['HOME'], ".siege", "addons"))

