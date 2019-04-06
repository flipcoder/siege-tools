#!/usr/bin/env python
import os
import sgmake
import subprocess
import json
from common import Status
from common import Settings
from common import Support
from common import call

def make(project):
    try:
        project.yarnpath = os.path.abspath(os.path.expanduser(Settings.get('yarn_path')))
    except:
        project.yarnpath = ""

    cmdline = [os.path.join(project.yarnpath,"yarn")]

    try:
        call(cmdline)
    except subprocess.CalledProcessError:
        return Status.FAILURE

    return Status.SUCCESS

def compatible(project):
    support = Support.ENVIRONMENT | Support.USER | Support.AUTO
    if os.path.isfile('package.json'):
        with open('package.json') as f:
            j = json.load(f)
            if u'engines' in j and u'yarn' in j[u'engines'].keys():
                support |= Support.PROJECT

    return support

