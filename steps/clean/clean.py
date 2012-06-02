#!/usr/bin/env python
import os
import sgmake
from common import Status
from common import Settings
from common import Support
from common import Args

def clean(project):
    # TODO Clean files and folders listed in project.clean
    #  Should obey wildcards (*) and recursive wildcards (**)

    try:
        for cmd in project.clean_commands:
            try:
                os.system(cmd)
            except:
                pass
    except:
        pass
    return Status.SUCCESS

def compatible(project):
    support = Support.ENVIRONMENT | Support.PROJECT # no auto

    if Args.option("rebuild"):
        support |= Support.USER

    return support

