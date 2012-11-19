#!/usr/bin/env python

import os
import sys

_program_name = None

def bit(x):
    return 1<<x

def mask(x):
    return (1<<x)-1

def set_program_name(name):
    global _program_name
    _program_name = name

def program_name():
    if not _program_name:
        return os.path.basename(sys.argv[0]).split('.')[0]
    else:
        return _program_name

class Status:
    UNSET=0
    SUCCESS=1
    FAILURE=2
    UNSUPPORTED=3

class Support:
    USER=bit(0) # settings specified in sgrc or provided by command line options
    PROJECT=bit(1) # settings specified in the project's sgrc or otherwise detected
    ENVIRONMENT=bit(2) # settings based on platform including limitations
    AUTO=bit(3) # allow automatic adds

    MASK=mask(4)


