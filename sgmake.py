#!/usr/bin/env python
"""Siege-Tools SiegeMake (\"sgmake\")
Multi-Language Build System Wrapper
Version 0.3.0
Copyright (c) 2012 Grady O'Connell
"""

import os, sys
from common import Args
from common import Settings

Args.valid_anywhere= ["help"]
Args.valid_options = ["version", "verbose", "strict"]
Args.valid_commands = ["list", "debug"]
Args.valid_keys = []
Args.command_aliases = {"?":"help", "ls":"list"}
Args.process()

def splash():
    print __doc__

def commands():
    print("Commands: %s" % ", ".join(Args.valid_commands))

def help():
    splash()
    commands()

class Status:
    UNSET=0
    SUCCESS=1
    FAILURE=2
    UNSUPPORTED=3

class Project:

    def __init__(self, filename):
        self.status = Status.UNSET
        self.name = os.path.basename(os.path.abspath(filename))
        self.filename = filename

    def run_user_script(self):
        ## Project config
        for fn in os.listdir("."):
            if (fn.lower()=="sg.py" or fn.lower().endswith(".sg.py")) and os.path.isfile(os.path.join(os.getcwd(), fn)):
                with open(fn) as source:
                    eval(compile(source.read(), fn, 'exec'), {}, self.__dict__)
    

    def complete(self):
        i = 1
        for step in ("clean","configure","make","obfuscate","sign","package","install"):
            step_name = step[0].upper() + step[1:]
            print "%s Step %s: %s..." % (self.name, i, step_name)
            i += 1
            status = getattr(self, step)()
            if status == Status.SUCCESS:
                print("%s finished." % step_name)
            elif status == Status.FAILURE:
                return False
            elif status == Status.UNSUPPORTED:
                print("%s unsupported." % step_name)

        return True

# TODO: separate language from system
class Java(Project):
    def __init__(self, fn):
        Project.__init__(self, fn)
        self.manifest = None
        self.name = os.path.basename(os.path.abspath(fn))
        self.sourcepath = ["src"]
        self.classpath = []
        self.obfuscator = None
        self.output = None
        self.build_sys = "java"

        self.run_user_script()

        self.status = Status.SUCCESS

    def clean(self):
        try:
            os.remove("dist"+os.sep+self.name+".jar")
        except OSError:
            pass
        return Status.SUCCESS

    def configure(self):
        if not os.path.isdir(os.path.join(os.getcwd(), "src")):
            return Status.FAILURE

        for folder in ("bin","dist"):
            try:
                os.mkdir(os.path.join(os.getcwd(), folder))
            except OSError:
                pass

        return Status.SUCCESS

    def make(self):
        classpath = ".";
        
        classpathlist = []
        classpathlist += ("lib", "libs")
        if self.classpath:
            classpathlist += self.classpath

        for entry in classpathlist:
            if os.path.isfile(entry):
                if classpath:
                    classpath = classpath + os.pathsep + entry
                else:
                    classpath = entry
                continue
            for (path, dirs, files) in os.walk(os.path.join(os.getcwd(), entry)):
                for fn in files:
                    if fn.lower().endswith(".jar"):
                        rel_path = os.path.relpath(path,fn)
                        rel_path = rel_path[len(os.pardir) + len(os.sep):len(rel_path)]
                        if classpath:
                            classpath = classpath + os.pathsep + os.path.join(rel_path,fn)
                        else:
                            classpath = os.path.join(rel_path,fn)

        if classpath:
            classpath = classpath + os.pathsep + os.pathsep.join(self.classpath)
        else:
            classpath = string.join(self.classpath,os.pathsep)

        sourcepath = ""

        for entry in self.sourcepath:
            if os.path.isfile(entry):
                if sourcepath:
                    sourcepath = sourcepath + os.linesep + os.path.join(rel_path,fn)
                else:
                    sourcepath = os.path.join(rel_path,fn)
                continue
            for (path, dirs, files) in os.walk(os.path.join(os.getcwd(), entry)):
                for fn in files:
                    if fn.lower().endswith(".java"):
                        rel_path = os.path.relpath(path,fn)
                        rel_path = rel_path[len(os.pardir) + len(os.sep):len(rel_path)]
                        if sourcepath:
                            sourcepath = sourcepath + " " + os.path.join(rel_path,fn)
                        else:
                            sourcepath = os.path.join(rel_path,fn)

        self.javapath = Settings.get('java_path')
        if self.javapath:
            if self.javapath[-1] != os.sep and os.altsep and Settings.get('java_path')[-1] != os.altsep:
                self.javapath += os.sep
        else:
            self.javapath = ""

        self.output = "dist"+os.sep+self.name+".jar"

        # TODO: boostrap class path
        os.system("%sjavac -Xlint:unchecked -source 1.6 -target 1.6 -d bin %s -cp %s" % (self.javapath, sourcepath, classpath))
        os.system("%sjar cmf %s "%(self.javapath, self.manifest)+"%s -C bin ." % (self.output))
        
        if not os.path.isfile(self.output):
            return Status.FAILURE

        return Status.SUCCESS

    def obfuscate(self):
        if self.obfuscator: # obfuscator used for project
            #try:
            obf_path = Settings.get("%s_path" % self.obfuscator)
            obf_path = os.path.abspath(obf_path)
            print self.javapath + "java -jar " + obf_path
            if not os.path.isfile(obf_path):
                return Status.FAILURE
            os.system(self.javapath + "java -jar " + obf_path + " " + self.obfuscator_params)
            #except:
            #    return Status.UNSUPPORTED

            return Status.SUCCESS

        return Status.UNSUPPORTED

    def sign(self):
        try:
            os.system("%sjarsigner -storepass %s %s %s" % (self.javapath, Settings.get("keystore_pass"), self.output, Settings.get("keystore_name")))
            
            # sign libs too (TODO: make optional)
            for classpath_dir in self.classpath:
                for fn in os.listdir(classpath_dir):
                    if fn.lower().endswith(".jar"):
                        os.system("%sjarsigner -storepass %s %s %s" % (self.javapath, Settings.get("keystore_pass"), os.path.join(classpath_dir,fn), Settings.get("keystore_name")))
                            
                            
            # TODO: if system call returns with error, then return Status.FAILURE, regardless of --strict
        except:
            return Status.FAILURE if Args.options["strict"] else Status.UNSUPPORTED

        return Status.SUCCESS
    
    def package(self):
        return Status.UNSUPPORTED
    def install(self):
        return Status.UNSUPPORTED


def ProjectFactory(filename):
    for fn in os.listdir("."):
        if os.path.isfile(fn):
            fn_lower = fn.lower();
            # TODO: loop through all registered project (build) type addons and run their test
            if fn_lower.endswith(".mf"):
                project = Java(filename)
                if not project.manifest:
                    project.manifest = fn
                return project
            #elif fn_lower=="makefile":
            #    self.build_sys = "make"
            #    self.build_script = fn;
            #elif fn_lower=="premake4.lua" or fn_lower=="premake.lua":
            #    self.build_sys = "premake"
            #    self.build_script = fn;
            #elif fn_lower=="cmakelists.txt":
            #    self.build_sys = "cmake"
            #    self.build_script = fn;
    return None

def try_project(fn):
    project = ProjectFactory(fn)

    if project and not project.status == Status.UNSUPPORTED:
        print "%s [%s]" % (project.name, project.build_sys)

    # only list details on list command
    if Args.command("list"):
        return 0

    if project and not project.status == Status.UNSUPPORTED:
        return 1 if project.complete() else -1

    return 0

def main():

    if Args.option("version"):
        splash()
        return
    if Args.anywhere("help") or Args.anywhere("?"):
        help()
        return

    wdir = os.getcwd();
    success_count = 0
    failed_count = 0

    r = try_project(".");
    if r == 1:
        success_count += 1
    elif r == -1:
        failed_count += 1

    # recurse once if no project
    if r == 0:
        for fn in os.listdir("."):
            if fn.startswith("."):
                continue
            if not os.path.isdir(os.path.join(wdir, fn)):
                continue
            if os.path.islink(os.path.join(wdir, fn)):
                continue

            os.chdir(os.path.join(wdir, fn));
            r = try_project(fn);
            if r == 1:
                success_count += 1
            elif r == -1:
                failed_count += 1

            os.chdir(wdir)

    if not Args.command("list"):
        if failed_count:
            print("%s project(s) failed." % failed_count)
        else:
            print("%s project(s) completed." % success_count)

if __name__ == "__main__":
    main()

