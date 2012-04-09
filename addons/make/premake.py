#!/usr/bin/env python
import os
import sgmake
from sgmake import Status
from common import Settings

def make(project):
    project.makepath = Settings.get('make_path')
    if project.makepath:
        if project.makepath[-1] != os.sep and os.altsep and Settings.get('make_path')[-1] != os.altsep:
            project.makepath += os.sep
    else:
        project.makepath = ""

    premake = ""
    if os.path.isfile("premake4.lua"):
        premake = "premake4"
    elif os.path.isfile("premake.lua"):
        premake = "premake"

    premake_platform = "gmake"

    os.system("%s%s %s" % (project.makepath, premake, premake_platform))
    return Status.SUCCESS

def update(project):
    # make sure theres a make step after premake
    make_step = ("make","make")
    clean_step = ("clean", "clean")
    if make_step in project.steps:
        project.steps.remove(make_step)
    if clean_step in project.steps:
        project.steps.remove(clean_step)
    i = 0
    for s in project.steps:
        i += 1
        if s[0] == "make" and s[1] == "premake":
            project.steps.insert(i,clean_step)
            project.steps.insert(i+1, make_step)
            break

def compatible(project):
    if os.path.isfile("premake.lua") or os.path.isfile("premake4.lua"):
        return True
    return False

