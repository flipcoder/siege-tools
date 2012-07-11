#!/usr/bin/python2
"""
Siege-Tools SiegeMake (\"sgmake\")
Multi-Language Extensible Build Automation
Version 0.5.0
Copyright (c) 2012 Grady O'Connell
"""

import os, sys
from common import Args
from common import Status
from common import Support
from common.Plugin import Plugin
import steps

def splash():
    print __doc__.strip()

def commands():
    print("Commands: %s" % ", ".join(Args.valid_commands))

def help():
    splash()
    print()
    commands()

def confirm(question, default="y"):
    default = default.lower()
    if default=="y":
        options="Y/n"
    else:
        options="y/N"
    # TODO: make this a single character read (no endline)
    choice = raw_input("%s (%s)? " % (question, options))
    choice = choice.lower()
    if choice == "":
        choice = default
    return choice=="y"

class Project(object):

    def __init__(self):
        self.status = Status.UNSET
        self.steps = []

    def run_user_config(self, config):
        for fn in os.listdir("."):
            if (fn.lower()==config or fn.lower().endswith(".%s" % config)) and os.path.isfile(os.path.join(os.getcwd(), fn)):
                # move config options into self.__dict__
                pass
    
    def run_user_script(self, script):
        ## Project config
        for fn in os.listdir("."):
            if (fn.lower()==script or fn.lower().endswith(".%s" % script)) and os.path.isfile(os.path.join(os.getcwd(), fn)):
                if not Args.option("warn") or confirm("Run potentially insecure python script \"%s\"" % fn, "y"):
                    with open(fn) as source:
                        eval(compile(source.read(), fn, 'exec'), {}, self.__dict__)
                else:
                    sys.exit(1)
    
    def complete(self):
        self.run_user_config("sg.ini")
        self.run_user_script("sg.py")

        # update all plugins after script runs
        for step in self.steps:
            step.call("update", self)
            #steps.update(step.type(), step.name(), self)

        i = 1
        for step in self.steps:
            step_type = step.type[0].upper() + step.type[1:] # capitalize step name
            print "%s step (addon: %s)..." % (step_type,  step.name)
            i += 1
            #status = getattr(self, step)()
            status = step.call(step.type, self) # example: install plugins call install() method
            #status = steps.step(step.type, step.name, self)
            #if status == Status.SUCCESS:
            #    #print("...%s finished." % step_name)
            if status == Status.FAILURE:
                print("...%s failed." % step_type)
                return False
            elif status == Status.UNSUPPORTED:
                print("...%s unsupported." % step_type)

        return True


def detect_project():

    #for addon in steps.base.values():
    #    try:
    #        if addon.Project.compatible():
    #            return addon.Project()
    #    except:
    #        pass

    project = Project()

    # Run all detection steps
    for addon in steps.steps["detect"]:
        if not Plugin("steps", "detect", addon).call("detect",project):
            return None
        #if not steps.step("detect", addon, project):

    # Add required steps to project
    for addon_type in steps.steps.iterkeys():
        if addon_type == "detect":
            continue
        for addon in steps.steps[addon_type]:
            #if steps.compatible(addon_type, addon, project) & Support.MASK == Support.MASK:
            plugin = Plugin("steps", addon_type, addon)
            if plugin.call("compatible", project) == Support.MASK:
                project.steps += [plugin]

    # check if project meets standards for a sgmake project
    if is_project(project):
        return project
    
    # otherwise, no project detected
    return None

# minimum requirements for a project
def is_project(project):
    for step in project.steps:
        if step.type in ("make","package"):
            return True
    return False

def try_project(fn):

    wdir = os.getcwd()

    if fn.startswith(".") and fn != ".": # check if path is hidden
        return 0
    if not os.path.isdir(os.path.join(wdir, fn)):
        return 0
    if os.path.islink(os.path.join(wdir, fn)):
        return 0

    os.chdir(os.path.join(wdir, fn))
    project = detect_project()

    if project and not project.status == Status.UNSUPPORTED:
        print "%s (%s)" % (project.name, os.path.relpath(os.getcwd(), wdir))

    # only list details on list command
    if Args.anywhere("list"):
        os.chdir(wdir)
        return 0

    if project and not project.status == Status.UNSUPPORTED:
        os.chdir(wdir)
        return 1 if project.complete() else -1

    os.chdir(wdir)
    return 0

def main():

    # option "interactive" is a placeholder and doesn't do anything yet
    Args.valid_options = ["list", "debug", "version", "verbose", "strict", "warn", "rebuild", "recursive"]#, "interactive", "recursive"
    Args.process()

    steps.process()

    if Args.option("version"):
        splash()
        return
    if Args.option("help") or Args.option("?"):
        help()
        return
    
    success_count = 0
    failed_count = 0

    if not Args.filenames:
        Args.filenames = ["."]

    for fn in Args.filenames:
        r = try_project(fn)
        if r == 1:
            success_count += 1
        elif r == -1:
            failed_count += 1

    # recurse once if no project
    #if r == 0:
    #    for fn in os.listdir("."):
    #        if fn.startswith("."):
    #            continue
    #        if not os.path.isdir(os.path.join(wdir, fn)):
    #            continue
    #        if os.path.islink(os.path.join(wdir, fn)):
    #            continue

    #        os.chdir(os.path.join(wdir, fn))

    #        r = try_project(fn)
    #        if r == 1:
    #            success_count += 1
    #        elif r == -1:
    #            failed_count += 1

    #        os.chdir(wdir)

    if not Args.command("list"):
        if failed_count:
            print("%s project(s) failed." % failed_count)
        elif success_count:
            print("%s project(s) completed." % success_count)
        else:
            print("Nothing to be done.")


if __name__ == "__main__":
    main()

