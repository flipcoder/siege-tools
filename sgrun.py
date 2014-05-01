#!/usr/bin/env python2
import os
import sys
import subprocess
exes = []
cwd = "."

class Break(Exception): pass

p = os.path.abspath(".")
try:
    while True:
        try:
            cwd = os.path.join(p, "bin")
            for f in os.listdir(cwd):
                fn = os.path.join(p, "bin/%s" % f)
                if not os.path.isdir(fn) and not "." in f and os.access(fn, os.X_OK):
                    exes += [f]
            if exes:
                raise Break
        except OSError:
            pass

        try:
            cwd = p
            for f in os.listdir(p):
                fn = f
                if not os.path.isdir(fn) and not "." in f and os.access(fn, os.X_OK):
                    exes += [f]
            if exes:
                raise Break
        except OSError:
            pass
        
        p = os.path.abspath(os.path.join(p, ".."))
        if p == "/":
            break
except Break:
    pass

# attempt to remove test executables that might be present in the current dir
if len(exes) > 1:
    exes_old = exes
    exes = [e for e in exes_old if "test" not in e.lower()]
    if len(exes) == 0:
        exes = exes_old # get the right error message

if len(exes) == 1:
    args = sys.argv[1:]
    if not args:
        args = []
    subprocess.call(['./'+exes[0]] + args, cwd=(cwd))
    #os.system(exes[0])
elif len(exes) > 1:
    print >> sys.stderr, "Too many executables"
    exit(1)
else:
    print >> sys.stderr, "No executables"
    exit(1)

