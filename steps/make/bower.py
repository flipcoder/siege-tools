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
        project.bowerpath = os.path.abspath(os.path.expanduser(Settings.get('bower_path')))
    except:
        project.bowerpath = ""

    cmdline = [os.path.join(project.bowerpath,"bower"), "install"]

    try:
        call(cmdline)
    except subprocess.CalledProcessError:
        return Status.FAILURE

    return Status.SUCCESS

def compatible(project):
    support = Support.ENVIRONMENT | Support.USER | Support.AUTO
    if os.path.exists("bower.json") or os.path.exists(".bowerrc"):
        support |= Support.PROJECT
    return support

