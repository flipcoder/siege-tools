#!/usr/bin/env python
import os
import sgmake
from sgmake import Status
from common import Settings

def make(project):
    project.javac_params = (project.javac_params if hasattr(project, "javac_params") else []) + ["-Xlint:unchecked"]
    return Status.UNSUPPORTED
    
def compatible(project):
    return False

