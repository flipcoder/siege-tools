#!/usr/bin/env python
import os
import sgmake
import subprocess
from common import Status
from common import Settings
from common import Support

def make(project):
    try:
        project.npmpath = os.path.abspath(os.path.expanduser(Settings.get('npm_path')))
    except:
        project.npmpath = ""

    #try:
    #    project.npm_params
    #except:
    #    project.npm_params = ""

    cmdline = [os.path.join(project.npmpath,"npm"), "install"]
    #if project.npm_params:
    #    cmdline += [project.makefile_params]

    #print " ".join(cmdline)

    try:
        subprocess.check_call(cmdline)
    except subprocess.CalledProcessError:
        return Status.FAILURE

    #os.system("%s%s" %
    #    (os.path.join(project.makepath,"make"),
    #        " %s" % project.makefile_params
    #    )
    #)
    return Status.SUCCESS

def compatible(project):
    support = Support.ENVIRONMENT | Support.USER | Support.AUTO
    if os.path.isfile("package.json"):
        support |= Support.PROJECT
    return support

