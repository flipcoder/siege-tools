#!/usr/bin/env python
import os
import sgmake
from sgmake import Status
from common import Settings

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

