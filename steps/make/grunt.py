#!/usr/bin/env python
import os
import sgmake
import subprocess
from common import Status
from common import Settings
from common import Support

def make(project):
    try:
        project.gruntpath = os.path.abspath(os.path.expanduser(Settings.get('grunt_path')))
    except:
        project.gruntpath = ""

    #try:
    #    project.grunt_params
    #except:
    #    project.grunt_params = ""

    cmdline = [os.path.join(project.gruntpath,"grunt")]
    #if project.grunt_params:
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
    if os.path.isfile("Gruntfile.js") or os.path.isfile("Gruntfile.coffee"):
        support |= Support.PROJECT
    return support

