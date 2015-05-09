#!/usr/bin/env python
import sys, os, imp
import collections
import importlib

base = {}
#steps = {}
plugins = collections.OrderedDict([
    ("detect", {}),
    ("analyze", {}),
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
ignore_steps = []
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
    global ignore_steps

    if not os.path.exists(path):
        return
    if not os.path.abspath(path) in sys.path:
        sys.path.append(path)
    #if not os.path.abspath(os.path.join(path,"steps")) in sys.path:
    #    sys.path.append(os.path.join(path,"steps"))

    for addon_type in steps:
        # addons can still be imported by other plugins even with this check, so plugins are still required to check .ignored(step) before adding
        if addon_type in ignore_steps:
            continue

        #if addon_type not in steps:
        #    steps[addon_type] = {}
        for step_addon in os.listdir(os.path.join(path,addon_type)):
            if step_addon in ignore_steps:
                continue

            name = step_addon
            if not name.islower():
                continue
            if name.endswith(".pyc"):
                continue
            if name == "__init__.py":
                continue
            if name.endswith(".py"):
                name = step_addon[:-3]
            elif not os.path.isdir(name):
                continue
            #steps[addon_type][name] = __import__(addon_type, globals(), locals(), [name], -1)
            try:
                steps[addon_type][name] = importlib.import_module("%s.%s" % (addon_type, name))
            except ImportError as e:
                print >> sys.stderr, "Missing dependency for addon \'%s\': %s" % (name, e.message)

def process():
    process_path(os.path.dirname(os.path.realpath(__file__)))

def ignore(step_names):
    global ignore_steps
    ignore_steps += step_names

def ignored(step):
    global ignore_steps
    if step in ignore_steps:
        return True
    return False

