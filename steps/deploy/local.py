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
    # TODO: check for user support -> return Support.USER
    return 0
