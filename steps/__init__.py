#!/usr/bin/env python
import sys, os, imp
import collections
import importlib

base = {}
#steps = {}
plugins = collections.OrderedDict([
    ("detect", {}),
    ("clean", {}),
    ("preprocess", {}),
    #("resolve", {}),
    ("make", {}),
    ("obfuscate", {}),
    ("doc", {}),
    ("sign", {}),
    ("package", {}),
    ("install", {}),
    ("test", {}),
    ("deploy", {})
    #("notify", {})
])
steps = plugins
#step_names = (
#    "detect",
#    "clean",
#    "preprocess",
#    "resolver",
#    "make",
#    "obfuscate",
#    "doc",
#    "sign",
#    "package",
#    "install",
#    "test",
#    "deploy",
#    "notify"
#)

#def step(group, addon, project):
#    if group in steps and addon in steps[group]:
#        try:
#            return getattr(steps[group][addon], group)(project)
#        except AttributeError:
#            pass
#    return 0

#def method(group, addon, method, project, default):
#    try:
#        return getattr(steps[group][addon], method)(project)
#    except AttributeError:
#        pass
#    return default

#def method2(group, addon, method, project, user, default):
#    try:
#        return getattr(steps[group][addon], method)(project,user)
#    except AttributeError:
#        pass
#    return default

#def compatible(group, addon, project):
#    r = method(group,addon,"compatible",project,-1)
#    if r == -1:
#        print "Warning: addon %s had an error." % addon
#    return r

#def update(group, addon, project):
#    return method(group,addon,"update",project,None)

def process_path(path):
    global base
    global steps

    if not os.path.exists(path):
        return
    if not os.path.abspath(path) in sys.path:
        sys.path.append(path)
    #if not os.path.abspath(os.path.join(path,"steps")) in sys.path:
    #    sys.path.append(os.path.join(path,"steps"))

    for addon_type in steps:
        #if addon_type not in steps:
        #    steps[addon_type] = {}
        for step_addon in os.listdir(os.path.join(path,addon_type)):
            name = step_addon
            if not name.islower():
                continue
            if name.endswith(".pyc"):
                continue
            if name == "__init__.py":
                continue
            if name.endswith(".py"):
                name = step_addon[:-3]
            elif not path.isdir(name):
                continue
            #steps[addon_type][name] = __import__(addon_type, globals(), locals(), [name], -1)
            steps[addon_type][name] = importlib.import_module("%s.%s" % (addon_type, name))

def process():
    process_path(os.path.dirname(os.path.realpath(__file__)))
    #process_path(os.path.join(os.environ['HOME'], ".siege", "steps"))


