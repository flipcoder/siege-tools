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

    if os.path.isfile("Gruntfile.ls"):
        try:
            project.lscpath = os.path.abspath(os.path.expanduser(Settings.get('lsc_path')))
        except:
            project.lscpath = ""
        lscmd = [
            os.path.join(project.lscpath,"lsc"),
            "-c", "Gruntfile.ls"
        ]
        try:
            subprocess.check_call(lscmd)
        except subprocess.CalledProcessError:
            return Status.FAILURE


    #try:
    #    project.grunt_params
    #except:
    #    project.grunt_params = []

    cmdline = [os.path.join(project.gruntpath,"grunt")]
    #if project.grunt_params:
    #    cmdline += project.grunt_params

    #print " ".join(cmdline)

    try:
        subprocess.check_call(cmdline)
    except subprocess.CalledProcessError:
        return Status.FAILURE

    return Status.SUCCESS

def compatible(project):
    support = Support.ENVIRONMENT | Support.USER | Support.AUTO
    if os.path.exists("Gruntfile.js") or\
        os.path.exists("Gruntfile.coffee") or\
        os.path.exists("Gruntfile.ls"):
        support |= Support.PROJECT
    return support

