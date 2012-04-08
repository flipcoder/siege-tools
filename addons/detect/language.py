#!/usr/bin/env python
import os
import collections
from common import Status

def detect(project):
    project.extensions = collections.defaultdict(int)
    for (paths, dirs, files) in os.walk("."):
        for fn in files:
            try:
                project.extensions[os.path.splitext(fn)[1][1:].lower()] += 1
            except:
                pass
    return Status.SUCCESS

