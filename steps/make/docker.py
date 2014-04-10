#!/usr/bin/env python
import os
import sgmake
import subprocess
from common import Status
from common import Settings
from common import Support

def make(project):
    try:
        project.dockerpath = os.path.abspath(os.path.expanduser(Settings.get('docker_path')))
    except:
        project.dockerpath = ""
    
    #try:
    #    project.sudocmd = os.path.abspath(os.path.expanduser(Settings.get('sudo_command')))
    #except:
    #    project.sudo_command = "sudo"

    cmdline = [
        os.path.join(project.dockerpath,"docker"),
        "-D=true",
        "build",
        "--no-cache",
        "-t=%s"%project.name,
        ".",
    ]

    #try:
    #    subprocess.check_call(os.path.join(project.dockerpath,"docker"), stdout=None, stderr=None)
    #except subprocess.CalledProcessError:
    #    pass

    # TODO: only do this next block if current user is not part of docker group
    #  or is not root 
    #print "Docker needs root permissions (C-c to cancel)"
    #cmdline = [project.sudo_command] + cmdline
    #project.event("status", "preauth")
    
    try:
        subprocess.check_call(cmdline)
    except subprocess.CalledProcessError:
        return Status.FAILURE

    return Status.SUCCESS

def compatible(project):
    support = Support.ENVIRONMENT | Support.USER | Support.AUTO
    if os.path.isfile("Dockerfile"):
        support |= Support.PROJECT
    return support

