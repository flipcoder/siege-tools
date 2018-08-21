#!/usr/bin/env python
import os
import sgmake
import subprocess
from common import Status
from common import Settings
from common import Support
from common import call

def make(project):
    try:
        project.npmpath = os.path.abspath(os.path.expanduser(Settings.get('npm_path')))
    except:
        project.npmpath = ""

    if os.path.isfile("package.json.ls") or os.path.isfile("package.lson"):
        
        try:
            project.lscpath = os.path.abspath(os.path.expanduser(Settings.get('lsc_path')))
        except:
            project.lscpath = ""
        
        if os.path.isfile("package.json.ls") :
            lscmd = [
                os.path.join(project.lscpath,"lsc"),
                "-jc", "package.json.ls"
            ]
        elif os.path.isfile("package.lson"):
            
            lscmd = [
                os.path.join(project.lscpath,"lsc"),
                "-jc", "package.lson"
            ]

        try:
            call(lscmd)
        except subprocess.CalledProcessError:
            return Status.FAILURE

    #try:
    #    project.npm_params
    #except:
    #    project.npm_params = []

    cmdline = [os.path.join(project.npmpath,"npm"), "install"]
    #if project.npm_params:
    #    cmdline += project.npm_params

    #print " ".join(cmdline)

    try:
        call(cmdline)
    except subprocess.CalledProcessError:
        return Status.FAILURE

    return Status.SUCCESS

#def update(project):
    #if os.path.isfile("package.json.ls") or os.path.isfile("package.lson"):
    #    # remove temp generated package.json
    #    project.clean += ['package.json']
    #    pass
    
def compatible(project):
    support = Support.ENVIRONMENT | Support.USER | Support.AUTO
    if os.path.isfile("package.json") or \
        os.path.isfile("package.json.ls") or \
        os.path.isfile("package.lson"):
        support |= Support.PROJECT
    return support

