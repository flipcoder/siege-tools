#!/usr/bin/env python
import os
import sgmake
from sgmake import Status
from common import Settings

def make(project):
    premake = ""
    if os.path.isfile("premake4.lua"):
        premake = "premake4"
    elif os.path.isfile("premake.lua"):
        premake = "premake"

    premake_platform = "gmake"

    os.system("%s %s" % (os.path.join(project.makepath, premake), premake_platform))
    return Status.SUCCESS

def update(project):
    project.makepath = os.path.abspath(os.path.expanduser(Settings.get('make_path'))) # TEMP

    # make sure theres a make step after premake
    make_step = Plugin("steps", "make", "make")
    project.clean_commands = ["%smake clean" % project.makepath]
    clean_step = Plugin("steps","clean", "clean")
    if make_step in project.steps:
        project.steps.remove(make_step)
    if clean_step in project.steps:
        project.steps.remove(clean_step)
    i = 0
    for s in project.steps:
        i += 1
        if s.type == "make" and s.name == "premake":
            project.steps.insert(i,clean_step)
            project.steps.insert(i+1, make_step)
            break

def compatible(project):
    if os.path.isfile("premake.lua") or os.path.isfile("premake4.lua"):
        return True
    return False

