#!/usr/bin/python2
"""
Siege-Tools SiegeMake (\"sgmake\")
Multi-Language Extensible Build Automation
Version 0.6.0
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
    """
    Detects the projects build steps and checks for step support
    """

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
    """
    Checks if a project meets the minimum step standards
    """
    for step in project.steps:
        if step.type in ("make","package"): # at least one make or package step
            return True
    return False


def try_project(fn):
    """
    Calls necessary detection methods on a potential project path
    Parameter is an os.path
    """
    # save previous dir so we can pop back into it
    wdir = os.getcwd()

    if fn.startswith(".") and fn != "." and fn != "..": # check if path is hidden
        return 0
    if not os.path.isdir(os.path.join(fn)):
        return 0
    if os.path.islink(fn):
        return 0

    # push new dir
    os.chdir(fn)
    project = detect_project()

    listed = False
    if project and not project.status == Status.UNSUPPORTED:
        print "%s (%s)" % (project.name, os.path.relpath(os.getcwd(), wdir))
        listed = True

    if Args.anywhere("list"):
        os.chdir(wdir)
        return 1 if listed else 0

    if listed:
        if project.complete():
            os.chdir(wdir)
            return 1
        else:
            os.chdir(wdir)
            return -1

    os.chdir(wdir)
    return 0


def main():
    # option "interactive" is a placeholder and doesn't do anything yet
    Args.valid_options = ["list", "debug", "version", "verbose", "strict", "warn", "recursive", "reversive", "execute", "x"] #, "interactive"
    Args.valid_keys = ["ignore"]
    Args.process()

    # process the build step plugins
    try:
        steps.ignore(Args.value("ignore").split(",")) # disable requested steps
    except AttributeError:
        pass
    steps.process()

    if Args.option("version"):
        splash()
        return
    if Args.option("help") or Args.option("?"):
        help()
        return
    
    # count of projects succeeded and failed
    success_count = 0
    failed_count = 0

    # if no project filenames are specified, we'll use the current directory (".")
    if not Args.filenames:
        Args.filenames = ["."]

    # check for forward recusion and backward scan settings
    recursive = Args.option("recursive")
    reversive = Args.option("reversive")
    execute = Args.option("x") or Args.option("execute")

    if recursive:
        # TODO this recursion sucks, fix it later
        # recurse through directories until you find project(s)
        for fn in Args.filenames:
            if fn.startswith(".") and fn != "." and fn != "..":
                continue
            r = 0
            for root, dirs, files in os.walk(fn):
                stop_recurse = False
                for d in dirs:
                    base =  os.path.basename(os.path.join(root,d))
                    if base.startswith(".") and base != ".":
                        continue

                    #print os.path.normpath(os.path.join(root,d))
                    r = try_project(os.path.normpath(os.path.join(root, d)))
                    if r == 1:
                        if not Args.option("list"):
                            success_count += 1
                        stop_recurse = True
                    elif r == -1:
                        if not Args.option("list"):
                            failed_count += 1
                if stop_recurse:
                    dirs[:] = []
                
    elif reversive:
        # TODO search for project by iterating dirs backwards
        # To be used build a sgmake project from within a nested directory or source editor

        for fn in Args.filenames:
            path = os.path.abspath(os.path.join(os.getcwd(), fn))
            while os.path.realpath(path) != os.path.realpath(os.path.join(path, "..")): # is root

                r = try_project(os.path.normpath(path))
                if r == 1:
                    if not Args.option("list"):
                        success_count += 1
                    break
                elif r == -1:
                    if not Args.option("list"):
                        failed_count += 1
                    break

                path = os.path.realpath(os.path.join(path, ".."))
            print "done: %s" % path
    else:
        # try to build projects specified by the user, current dir is default
        for fn in Args.filenames:
            r = try_project(os.path.join(os.getcwd(),fn))
            if r == 1:
                success_count += 1
            elif r == -1:
                failed_count += 1


    if not Args.command("list"):
        # if not in list-only mode, display final status of built projects
        if failed_count:
            print("%s project(s) failed." % failed_count)
        elif success_count:
            print("%s project(s) completed." % success_count)
        else:
            print("Nothing to be done.")


if __name__ == "__main__":
    main()

