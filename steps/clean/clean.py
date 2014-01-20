#!/usr/bin/env python
import os
import sgmake
from common import Status
from common import Settings
from common import Support
from common import Args

def clean(project):
    # if added from another plug-in update may not be called
    # TODO: this is hackish fix, but it'll do for now
    try:
        project.clean_commands
    except:
        project.clean_commands = []

    for cmd in project.clean_commands:
        try:
            os.system(cmd)
        except:
            pass

    # TODO: parse wildcards and recursive wildcards

    #for path in project.clean:
    #    print "Removing %s..." % path
    #    os.remove(path)

    return Status.SUCCESS

def update(project):
    project.clean = []
    project.clean_commands = []

def compatible(project):
    support = Support.ENVIRONMENT | Support.PROJECT # no auto

    if Args.option("clean"):
        support |= Support.USER

    return support

