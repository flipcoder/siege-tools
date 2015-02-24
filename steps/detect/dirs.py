#!/usr/bin/env python
import os
import collections
from common import Status

def detect(project):
    # TODO: detect dirs
    try:
        # allow overriding name
        project.name
    except:
        project.name = os.path.basename(os.path.abspath(os.getcwd()))
    project.sourcepath = ["src"]
    return Status.SUCCESS

