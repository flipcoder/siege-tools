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

    try:
        project.makepath = os.path.abspath(os.path.expanduser(Settings.get('make_path')))
    except:
        project.makepath = ""

    # TODO: detect a suitable vcvars if the environment isnt init

    cmdline = [os.path.join(project.makepath,"msbuild")]
    cmdline += ["/p:Platform=Win32"]
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
        # no need to generate params, we're done
        return
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
        project.msbuild_params += [project.name+".sln"]
    else:
        project.msbuild_params += [projname]


def compatible(project):
    support = Support.USER
    
    for fn in os.listdir(os.getcwd()):
        if os.path.isfile(os.path.join(os.getcwd(),fn)):
            fnl = fn.lower()
            if fnl.endswith(".sln"):
                support |= Support.PROJECT
                support |= Support.AUTO

    if os.name=="nt":
        support |= Support.ENVIRONMENT
    
    return support

