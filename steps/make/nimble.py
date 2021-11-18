#!/usr/bin/env python
import os
import sgmake
from common import Status
from common import Support
from common import Settings
from common import Args
from common.Plugin import Plugin
import subprocess
from common import call


def make(project):

    cmd = [
        "nimble",
    ]
    if Args.option("debug"):
        cmd.append("build")
    else:
        cmd.append("install")

    try:
        call(cmd)
    except subprocess.CalledProcessError:
        return Status.FAILURE

    return Status.SUCCESS


def update(project):
    # TODO: add exe's in all bin/ folders to be cleaned
    pass


def compatible(project):
    support = Support.ENVIRONMENT | Support.USER | Support.AUTO

    for fn in os.listdir(os.getcwd()):
        if os.path.isfile(os.path.join(os.getcwd(), fn)):
            if fn.lower().endswith(".nimble"):
                nimble = os.path.join(os.getcwd(), fn)
                project.nimble = nimble
                support |= Support.PROJECT
                break

    return support
