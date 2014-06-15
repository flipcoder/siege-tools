#!/usr/bin/env python
import os
import sgmake
from common import Status
from common import Support
from common import Settings
from common.Plugin import Plugin
import shutil
import clean.clean

def generate(project): # can throw
    tmpl = os.path.join(os.path.split(__file__)[0], "premake/premake4.lua")
    print tmpl
    fn = os.path.join(os.getcwd(), "premake4.lua")
    dest = open(fn, "w")
    #shutil.copy2(tmpl, os.getcwd())
    with open(tmpl) as f:
        for line in f.readlines():
            line = line.replace("PROJECT_NAME", project.name)
            dest.write(line + "\n")
            pass

def make(project):
    
    premake = ""
    if os.path.isfile("premake4.lua"):
        premake = "premake4"
    elif os.path.isfile("premake.lua"):
        premake = "premake"

    try:
        project.premake_platform
    except:
        project.premake_platform = "gmake"

    premake_platform_param = ""
    try:
        if project.premake_platform:
            premake_platform_param = "--platform=%s" % project.platform_param
    except:
        pass

    os.system("%s %s %s" % (os.path.join(project.makepath, premake), project.premake_platform, premake_platform_param))
    return Status.SUCCESS

def update(project):
    try:
        project.generate
    except:
        project.generate = []
    
    if "premake" in project.generate:
        generate(project) # can throw
    
    try:
        project.makepath = os.path.abspath(os.path.expanduser(Settings.get('make_path')))
    except:
        project.makepath = ""
    # make sure theres a make step after premake

    make_step = Plugin("steps", "make", "makefile")
    project.clean_commands = ["%s clean" % os.path.join(project.makepath,"make")]
    clean_step = Plugin("steps", "clean", "clean")
    if make_step in project.steps:
        project.steps.remove(make_step)
    if clean_step in project.steps:
        project.steps.remove(clean_step)

    i = 0
    for s in project.steps:
        if s.type == "make" and s.name == "premake":
            # TODO: check for user support (because of -r flag)
            if clean.clean.compatible(project) & Support.USER:
                project.steps.insert(i, clean_step)
                project.steps.insert(i+2, make_step)
            else:
                project.steps.insert(i+1, make_step)
            break
        i += 1

def compatible(project):
    support = Support.MASK & (~Support.PROJECT)
    try:
        project.generate
    except:
        project.generate = []
    
    try:
        if "premake" in project.generate:
            support |= Support.PROJECT
    except:
        pass
    
    if os.path.isfile("premake.lua") or os.path.isfile("premake4.lua"):
        support |= Support.PROJECT
    return support

