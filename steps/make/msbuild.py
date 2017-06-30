#!/usr/bin/env python
import os
import sgmake
import multiprocessing
import subprocess
import tempfile
import math
from common import Status
from common import Settings
from common import Support
from common.Plugin import Plugin

def make(project):

    # TODO: if only one project exists, specify it as param to msbuild
    # otherwise, build main proj

    # project.msbuild_params += "test.vcxproj"

    # TODO: detect a suitable vcvars if the environment isnt init
    
    cmdline = [os.path.join(project.makepath,"msbuild")]
    if project.msbuild_params:
        cmdline += project.msbuild_params

    try:
        os.chdir(project.build_dir)
    except:
        pass
    
    try:
        subprocess.check_call(cmdline)
    except subprocess.CalledProcessError:
        try:
            if project.build_dir:
                os.chdir("..")
        except:
            pass
        return Status.FAILURE
    
    try:
        if project.build_dir:
            os.chdir("..")
    except:
        pass

    return Status.SUCCESS

def update(project):
    
    # msbuild overrides makefile steps, since makefile is probably posix only
    make_step = Plugin("steps", "make", "makefile")
    if make_step in project.steps:
        project.steps.remove(make_step)

    # TODO: check for user provided filename before overriding, if it exists, skip this step and the ls
    try:
        project.msbuild_params
    except:
        project.msbuild_params = []

    projname = ""
    projs = 0
    for fn in os.listdir(os.getcwd()):
        if os.path.isfile(os.path.join(os.getcwd(),fn)):
            fnl = fn.lower()
            if fnl.endswith(".sln"):
                projname = os.path.join(os.getcwd(), fn)
                projs += 1
                break
    
    if projs > 1:
        project.msbuild_params += [project.name]
    else:
        project.msbuild_params += [projname]


def compatible(project):
    support = Support.MASK & (~Support.PROJECT) & (~Support.ENVIRONMENT)
    if os.name=="nt":
        support |= Support.ENVIRONMENT
    if os.path.isfile("Makefile"):
        support |= Support.PROJECT
    return support

