#!/usr/bin/env python
"""
Siege-Tools SiegeMake (\"sgmake\")
Multi-Language Build System Wrapper
Version 0.4.0
Copyright (c) 2012 Grady O'Connell
"""

import os, sys
from common import Args
from common import Settings
from common import Status
import addons

def splash():
    print __doc__.strip()

def commands():
    print("Commands: %s" % ", ".join(Args.valid_commands))

def help():
    splash()
    print()
    commands()

class Project(object):

    def __init__(self):
        self.status = Status.UNSET
        self.steps = []

    def run_user_script(self, script):
        ## Project config
        for fn in os.listdir("."):
            if (fn.lower()==script or fn.lower().endswith(".%s" % script)) and os.path.isfile(os.path.join(os.getcwd(), fn)):
                with open(fn) as source:
                    eval(compile(source.read(), fn, 'exec'), {}, self.__dict__)
    
    def complete(self):
        self.run_user_script("sg.py")

        # update all plugins after script runs
        for step in self.steps:
            addons.update(step[0], step[1], self)

        i = 1
        for step in self.steps:
            step_name = step[0][0].upper() + step[0][1:] # capitalize step name
            print "%s step (addon: %s)..." % (step_name,  step[1])
            i += 1
            #status = getattr(self, step)()
            status = addons.step(step[0], step[1], self)
            #if status == Status.SUCCESS:
            #    #print("...%s finished." % step_name)
            if status == Status.FAILURE:
                return False
            elif status == Status.UNSUPPORTED:
                print("...%s unsupported." % step_name)

        return True


def detect_project():

    #for addon in addons.base.values():
    #    try:
    #        if addon.Project.compatible():
    #            return addon.Project()
    #    except:
    #        pass

    project = Project()
    # Run all detection addons
    for addon in addons.steps["detect"]:
        if not addons.step("detect", addon, project):
            return None
    # Add required steps to project
    for addon_type in addons.steps.iterkeys():
        if addon_type == "detect":
            continue
        for addon in addons.steps[addon_type]:
            if addons.compatible(addon_type, addon, project):
                project.steps += [(addon_type, addon)]

    # If project contains steps, its a project
    if project.steps:
        return project

    return None

def try_project(fn):

    project = detect_project()

    if project and not project.status == Status.UNSUPPORTED:
        print "[%s]" % project.name

    # only list details on list command
    if Args.command("list"):
        return 0

    if project and not project.status == Status.UNSUPPORTED:
        return 1 if project.complete() else -1

    return 0

def main():

    Args.valid_anywhere= ["help"]
    Args.valid_options = ["version", "verbose", "strict"]
    Args.valid_commands = ["list", "debug"]
    Args.valid_keys = []
    Args.command_aliases = {"?":"help", "ls":"list"}
    Args.process()

    addons.process()

    if Args.option("version"):
        splash()
        return
    if Args.anywhere("help") or Args.anywhere("?"):
        help()
        return

    wdir = os.getcwd()
    success_count = 0
    failed_count = 0

    r = try_project(".")
    if r == 1:
        success_count += 1
    elif r == -1:
        failed_count += 1

    # recurse once if no project
    if r == 0:
        for fn in os.listdir("."):
            if fn.startswith("."):
                continue
            if not os.path.isdir(os.path.join(wdir, fn)):
                continue
            if os.path.islink(os.path.join(wdir, fn)):
                continue

            os.chdir(os.path.join(wdir, fn))

            r = try_project(fn)
            if r == 1:
                success_count += 1
            elif r == -1:
                failed_count += 1

            os.chdir(wdir)

    if not Args.command("list"):
        if failed_count:
            print("%s project(s) failed." % failed_count)
        elif success_count:
            print("%s project(s) completed." % success_count)
        else:
            print("Nothing to be done.")


if __name__ == "__main__":
    main()

