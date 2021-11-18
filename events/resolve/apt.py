#!/usr/bin/env python
"""
Apt/Aptitude Dependency Resolver
"""
import os, sys
import subprocess
import sgmake
from sgmake import Status
from common import Settings

# dependency resolvers are silent steps, they are called by other steps as needed


def resolve(project, lib):
    name = resolver.simplify_package_name(lib)
    matches = subprocess.check_output(["apt-cache", "search", name])
    for m in matches.split(os.linesep):
        print(m)
    return None
    # TODO determine best match, run through project.resolver


def compatible(project):
    if not sys.platform.startswith("linux"):
        return False

    # Check for package program
    for path in os.environ["PATH"].split(os.pathsep):
        for program in ("apt-get", "aptitude"):
            if os.path.exists(os.path.join(path, program)):
                project.resolver = program
                return True

    return False
