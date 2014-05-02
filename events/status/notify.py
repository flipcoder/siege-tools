#!/usr/bin/env python2
from common import Status
from common import Settings
from common import Support
import os
import time

inited = False

def status(project, args):
    try:
        from gi.repository import Notify
    except:
        return
    
    global inited

    if not inited:
        Notify.init("sgmake")
        inited = True

    #if not "step" in args and not "start" in args:
    if "success" == args:
        Notify.Notification.new(
            "sgmake",
            "Build Complete",
            'dialog-information'
        ).show()
    
    if "failure" == args:
        Notify.Notification.new(
            "sgmake",
            "Build Failure",
            'dialog-error'
        ).show()

def compatible(project):
    try:
        from gi.repository import Notify
    except ImportError:
        return Support.MASK & ~Support.ENVIRONMENT
    return Support.MASK
