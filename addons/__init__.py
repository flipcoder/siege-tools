#!/usr/bin/env python
import sys, os, imp
import collections
import importlib

base = {}
#steps = {}
steps = collections.OrderedDict([
    ("detect", {}),
    ("clean", {}),
    ("preprocess", {}),
    ("resolver", {}),
    ("make", {}),
    ("obfuscate", {}),
    ("doc", {}),
    ("sign", {}),
    ("package", {}),
    ("install", {}),
    ("test", {}),
    ("deploy", {}),
    ("notify", {})
])
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

def step(group, addon, project):
    if group in steps and addon in steps[group]:
        if hasattr(steps[group][addon], group):
            return getattr(steps[group][addon], group)(project)
    return 0

def compatible(group, addon, project):
    #print steps[group][addon]
    #print "%s %s" % (group,addon)
    if hasattr(steps[group][addon], "compatible"):
        return getattr(steps[group][addon], "compatible")(project)
    return False

def update(group, addon, project):
    if hasattr(steps[group][addon], "update"):
        getattr(steps[group][addon], "update")(project)

# minimum requirements for a project
def is_project(project):
    for step in project.steps:
        if step[0] in ("make","package"):
            return True
    return False

def process_path(path):
    global base
    global steps

    if not os.path.exists(path):
        return
    if not os.path.abspath(path) in sys.path:
        sys.path.append(path)
    #if not os.path.abspath(os.path.join(path,"addons")) in sys.path:
    #    sys.path.append(os.path.join(path,"addons"))

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

    #for fn in os.listdir(path):
    #    if fn.lower().endswith(".py") and not fn.lower() == "__init__.py":
    #        name = fn[:-3]
    #        base[name] = __import__(name, globals(), locals(), [], -1)
    #        #if hasattr(base[fn],"category"): # TODO addon categories
    #    elif os.path.isdir(os.path.join(path,fn)):
    #        addon_type = fn.lower()
    #        if addon_type not in steps:
    #            steps[addon_type] = {}
    #        for step_addon in os.listdir(os.path.join(path,fn)):
    #            name = step_addon.lower()
    #            if name.endswith(".pyc"):
    #                continue
    #            if name == "__init__.py":
    #                continue
    #            if name.endswith(".py"):
    #                name = step_addon[:-3]
    #            steps[addon_type][name] = __import__("%s.%s" % (fn, name), globals(), locals(), [], -1)

def process():
    process_path(os.path.dirname(os.path.realpath(__file__)))
    #process_path(os.path.join(os.environ['HOME'], ".siege", "addons"))


