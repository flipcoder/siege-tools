#!/usr/bin/env python
import sys, os, imp

base = {}
steps = {}

def step(name, user_data):
    if name in steps and user_data in steps[name]:
        return getattr(steps[name][user_data], name)(user_data)
    return 0

def process_path(path):
    global base
    global steps

    if not os.path.exists(path):
        return
    if not os.path.abspath(path) in sys.path:
        sys.path.append(path)
    if not os.path.abspath(os.path.join(path,"steps")) in sys.path:
        sys.path.append(os.path.join(path,"steps"))

    for fn in os.listdir(path):
        if fn.lower().endswith(".py") and not fn.lower() == "__init__.py":
            name = fn[:-3]
            base[name] = __import__(name, globals(), locals(), [], -1)
            #if hasattr(base[fn],"category"): # TODO addon categories
        elif os.path.isdir(os.path.join(path,fn)):
            addon_type = fn.lower()
            if addon_type not in steps:
                steps[addon_type] = {}
            for step_addon in os.listdir(os.path.join(path,fn)):
                name = step_addon.lower()
                if name.endswith(".pyc"):
                    continue
                if name == "__init__.py":
                    continue
                if name.endswith(".py"):
                    name = step_addon[:-3]
                steps[addon_type][name] = __import__("%s.%s" % (fn, name), globals(), locals(), [], -1)

def process():
    process_path(os.path.dirname(os.path.realpath(__file__)))
    #process_path(os.path.join(os.environ['HOME'], ".siege", "addons"))


