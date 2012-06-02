"""
Dropbox-compatible autopush for completed packages
"""
import os
import sgmake
from common import Status
from common import Settings

def install(project):
    return Status.SUCCESS

def compatible(project):
    # only if user supports
    return False

