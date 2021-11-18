#!/usr/bin/env python
import sys, os, imp
import collections
import importlib

base = {}
# events = {}
events = collections.OrderedDict([("status", {})])
# event_names = (
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
# )


def event(group, addon, project):
    if group in events and addon in events[group]:
        try:
            return getattr(events[group][addon], group)(project)
        except:
            pass
    return 0


def method(group, addon, method, project, default):
    try:
        return getattr(events[group][addon], method)(project)
    except:
        pass
    return default


def method2(group, addon, method, project, user, default):
    try:
        return getattr(events[group][addon], method)(project, user)
    except:
        pass
    return default


def compatible(group, addon, project):
    return method(group, addon, "compatible", project, False)


# def update(group, addon, project):
#    return method(group,addon,"update",project,None)

# minimum requirements for a project
# def is_project(project):
#    for event in project.events:
#        if event[0] in ("make","package"):
#            return True
#    return False


def process_path(path):
    global base
    global events

    if not os.path.exists(path):
        return
    if not os.path.abspath(path) in sys.path:
        sys.path.append(path)
    # if not os.path.abspath(os.path.join(path,"events")) in sys.path:
    #    sys.path.append(os.path.join(path,"events"))

    for addon_type in events:
        # if addon_type not in events:
        #    events[addon_type] = {}
        for event_addon in os.listdir(os.path.join(path, addon_type)):
            name = event_addon
            if not name.islower():
                continue
            if name.endswith(".pyc"):
                continue
            if name == "__init__.py":
                continue
            if name.endswith(".py"):
                name = event_addon[:-3]
            elif not os.path.isdir(name):
                continue
            # events[addon_type][name] = __import__(addon_type, globals(), locals(), [name], -1)
            try:
                events[addon_type][name] = importlib.import_module(
                    "%s.%s" % (addon_type, name)
                )
            except ImportError:
                pass

    # for fn in os.listdir(path):
    #    if fn.lower().endswith(".py") and not fn.lower() == "__init__.py":
    #        name = fn[:-3]
    #        base[name] = __import__(name, globals(), locals(), [], -1)
    #        #if hasattr(base[fn],"category"): # TODO addon categories
    #    elif os.path.isdir(os.path.join(path,fn)):
    #        addon_type = fn.lower()
    #        if addon_type not in events:
    #            events[addon_type] = {}
    #        for event_addon in os.listdir(os.path.join(path,fn)):
    #            name = event_addon.lower()
    #            if name.endswith(".pyc"):
    #                continue
    #            if name == "__init__.py":
    #                continue
    #            if name.endswith(".py"):
    #                name = event_addon[:-3]
    #            events[addon_type][name] = __import__("%s.%s" % (fn, name), globals(), locals(), [], -1)


def process():
    process_path(os.path.dirname(os.path.realpath(__file__)))
    # process_path(os.path.join(os.environ['HOME'], ".siege", "events"))
