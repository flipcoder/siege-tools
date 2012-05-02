#!/usr/bin/env python
import os
import collections
from common import Status

def detect(project):
    # TODO: detect dirs
    project.name = os.path.basename(os.path.abspath(os.getcwd()))
    project.sourcepath = ["src"]
    return Status.SUCCESS

