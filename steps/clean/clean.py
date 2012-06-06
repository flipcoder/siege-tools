#!/usr/bin/env python
import os
import sgmake
from common import Status
from common import Settings
from common import Support
from common import Args

def clean(project):
    for cmd in project.clean_commands:
        try:
            os.system(cmd)
        except:
            pass

    for path in project.clean_paths:
        print "Removing %s..." % path
        os.remove(path)

    return Status.SUCCESS

def update(project):
    project.clean_paths = []
    project.clean_commands = []

def compatible(project):
    support = Support.ENVIRONMENT | Support.PROJECT # no auto

    if Args.option("rebuild"):
        support |= Support.USER

    return support

