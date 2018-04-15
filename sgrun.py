#!/usr/bin/env python2
import os
import sys
import re
import subprocess
import json
exes = []
cwd = "."
plugins = []
p = os.path.abspath(".")
foldername = ""
args = sys.argv[1:]
if not args:
    args = []

def path_equals(a, b):
    return os.path.normpath(os.path.expanduser(a)) == \
        os.path.normpath(os.path.expanduser(b))

def run():
    global args
    global exes
    r = 1
    
    if "---l" in args:
        print os.path.join(cwd,exes[0])
        return 0
    elif "---d" in args:
        print os.path.dirname(cwd)
        return 0
    else:
        args = [a for a in args if not a.startswith("---")]
        try:
            with open(os.path.join(cwd, os.path.dirname(exes[0]), "sg.json"), 'r') as f:
                j = json.load(f)
                args += j['args']
        except:
            pass
        
        if os.name=="nt":
            r = subprocess.call([os.path.join(cwd,exes[0])] + args, cwd=(cwd))
        else:
            r = subprocess.call(['./'+exes[0]] + args, cwd=(cwd))
    return r

def advanced():
    global exes
    global args
    global foldername

    if len(exes) == 1:
        return run()

    # plugin: project name hint
    try:
        if len(exes) > 1 and foldername:
            for exe in exes:
                if os.path.basename(exe) == foldername:
                    exes = [foldername]
                    return run()
    except:
        pass

    # TODO: plugin: package.json
    try:
        import json
        with open("package.json") as f:
            j = json.load(f)
            exe = j["main"] + ".js"
            if os.path.isfile(exe):
                exes = [exe]
                return run()
    except:
        pass

    # TODO: plugin: python
    # try:
    while True:
        pys = []
        for fn in os.listdir("."):
            fnl = fn.lower()
            # if fnl == "requirements.txt":
            #     if os.name == "nt":
            #         exes = ["python"] # TODO: version detection?
            if fnl.endswith(".py"):
                pys += [fn]

            if len(pys) == 1:
                pass
            elif len(pys) > 1:
                for py in pys:
                    if os.name == "nt":
                        exes = ["python"]
                        args = [fn] + args
                        break
                    else:
                        exes = [fn]
                        break
                
                    fn_noext = fn[:-3]
                    fn_noext_l = fn_noext.lower()
                    if fn_noext_l == "main" or  fnl_noext_l == foldername:
                        if os.name == "nt":
                            exes = ["python"]
                            args = [fn] + args
                            break
                        else:
                            exes = [fn]
                            break
        break


    # TODO: plugin: expression match
    while True:
        use_regex = False
        idx = -1
        try:
            idx = args.index("---e")
            use_regex = True
        except:
            pass
        if idx == -1:
            try:
                idx = args.index("---n")
                use_regex = False
            except:
                pass
        if idx == -1:
            break
        try:
            expr = args[idx+1]
        except:
            print >> sys.stderr, "---e flag needs expression param"
            return 1

        del args[idx+1]
        del args[idx]
        if not use_regex:
            if expr not in exes:
                print >> sys.stderr, "\"%s\" does not exist" % expr
                return 1
            exes = [expr]
            return run()
        else: # regex
            exes = [e for e in exes if re.search(expr, e)]
            if exes:
                return advanced()
            else:
                print >> sys.stderr, "No executables matching expression"
                return 1
        break
    
    # plugin: ignore tests
    if len(exes) > 1:
        exes_old = exes[:]
        exes = [e for e in exes_old if "test" not in e.lower()]
        if len(exes) == 1:
            exit(run())
        else:
            # restore and continue
            exes = exes_old
    
    if len(exes) > 1:
        print >> sys.stderr, 'Found %s executables: %s' % (len(exes), ', '.join(exes))
        print >> sys.stderr, "Too many executables"
    elif len(exes) == 0:
        print >> sys.stderr, "No executables"
    return 1
    
class Break(Exception): pass

def exe(fn):
    if os.path.isdir(fn):
        return False
    if os.name=='nt':
        return fn.lower().endswith(".exe")
    else:
        return os.access(fn, os.X_OK)

p = os.path.abspath(".")
try:
    while True:
        try:
            cwd = os.path.join(p, "bin")
            for f in os.listdir(cwd):
                fn = os.path.join(p, "bin/%s" % f)
                if exe(fn):
                    exes += [f]
            if exes:
                raise Break
        except OSError:
            pass

        try:
            cwd = p
            for f in os.listdir(p):
                fn = f
                if exe(fn):
                    exes += [f]
                    fnp = os.path.basename(os.getcwd())
                    if fnp == "bin":
                        fnp = os.path.basename(os.path.abspath(os.path.join(os.getcwd(), "..")))
                    foldername = os.path.join(os.path.basename(fnp))
            if exes:
                raise Break
        except OSError:
            pass

        p = os.path.abspath(os.path.join(p, ".."))
        if p == "/" or path_equals(p,"~") or path_equals(p,"~/bin"):
            break
except Break:
    pass

exit(advanced())

