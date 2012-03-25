#!/usr/bin/env python
import os, sys

PROGRAM_NAME = "Siege-Tools SiegeMake (\"sgmake\")"
PROGRAM_VERSION = "0.1"
PROGRAM_COPYRIGHT = "Copyright (c) 2012 Grady O'Connell"

user_settings = {}

# sgmake option
# sgmake --command
# sgmake -a
# sgmake --mapkey=mapvalue

app_options = []
app_commands = []
app_arg_map = {}

# arg 'anywhere' means either option or command, both work
app_valid_anywhere = ["help", "?"]
app_valid_options = app_valid_anywhere + ["version", "verbose", "strict"]
app_valid_keys = ["generate"]
app_valid_commands = app_valid_anywhere + ["list", "debug"]

app_command_alias = {"ls":"list"} # not yet implemented


def splash():
    print("%s %s" % (PROGRAM_NAME, PROGRAM_VERSION))
    print(PROGRAM_COPYRIGHT)
    print("See README for details.")

def commands():
    print("Commands: %s" % ", ".join(app_valid_commands))

def help():
    splash()
    print("")
    commands()


def settings_load(fn):
    try:
        fn = os.environ['HOME']+os.sep+fn
        with open(fn) as source:
            eval(compile(source.read(), fn, 'exec'), {}, user_settings)
        return True
    except IOError:
        return False

for fn in (".sgrc.py", "_sgrc.py"):
    if settings_load(fn):
        break

def settings():
    return app_settings

def arg_option(s):
    if s in app_options:
        return True
    return False

def arg_value(s):
    if s in app_arg_map:
        return app_arg_map[s]
    return None

def arg_command(s):
    if s in app_commands:
        return True
    return False

def arg_anywhere(s):
    if s in app_commands or s in app_options:
        return True
    return False

for arg in sys.argv[1:]:
    arg = arg.lower()
    if arg.startswith("--"):
        if '=' in arg:
            idx = arg.find("=")
            key = arg[2:idx]
            try:
                value = arg[idx+1:]
            except:
                print "No key specified for parameter \'%s\'" % arg
                exit(1)
                #break
                
            if key not in app_valid_map:
                print "Invalid parameter \'%s\'" % arg
                exit(1)

            if key not in app_arg_map:
                app_arg_map[key] = value
            #app_options.append(key)
        else:
            if arg not in app_valid_options:
                print "Invalid parameter \'%s\'" % arg
                exit(1)
            if arg not in app_options:
                app_options.append(arg)
    elif arg.startswith("-"):
    #    arg = arg[1:]
    #    if arg in app_valid_options:
    #        app_options.append(arg)
    #    else:

        arg_letters = arg[1:]
        if (len(arg_letters) == 0):
            print "Invalid paramter \'%s\'" % arg
            exit(1)

        # if user passes something like -version ("anywhere" command), allow it as a normal parameter,
        # instead of each letter -v -e -r -s... etc.
        if arg_letters in app_valid_anywhere:
            app_options.append(arg_letters)
            continue

        # otherwise look through each letter for each parameter meaning
        for ch in arg_letters:
            matched_arg = False
            num_matches = 0
            for arg_name in app_options:
                if ch == arg_name[:1]:
                    if arg_name not in app_options:
                        app_options.append(arg_name)
                    matched_arg = True
                elif ch == arg_name[:1].upper():
                    # uses secondary match if the letter is capitalized
                    # example: -v matches version, -V matches verbose
                    if num_matches > 1: 
                        app_options.append(arg_name)
                        matched_arg
                    num_matches += 1
                    
            if not matched_arg:
                print "Invalid parameter \'-%s\'" % ch
                exit(1)

    else:
        # no prefix dashes (-) on argument means its an command/command
        if arg in app_valid_commands:
            app_commands.append(arg);
        else:
            print "Invalid command \'%s\'" % arg
            commands()
            exit(1)

class Status:
    UNSET=0
    SUCCESS=1
    FAILURE=2
    UNSUPPORTED=3

class BuildSystem(object):
    pass

class Java(BuildSystem):
    def __init__(self, project):
        self.manifest = None
        self.name = "java"
        self.project = project
        self.sourcepath = ["src"]
        self.classpath = []

    def __str__(self):
        return self.name

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
        

        #f = open("sg-cache"+os.sep+"classpath_file_list", "w");
        #f.write(classpath);
        #f.close()

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

        #f = open("sg-cache"+os.sep+"source_file_list", "w");
        #f.write(sourcepath);
        #f.close()

        #print(classpath_param)
        os.system("javac -Xlint:unchecked -source 1.6 -target 1.6 -d bin  %s -cp %s" % (sourcepath, classpath))
        os.system("jar cmf %s dist"%(self.manifest)+os.sep+"%s.jar -C bin ." % (self.name))
        return Status.SUCCESS

    def obfuscate(self):
        return Status.UNSUPPORTED

    def sign(self):
        try:
            os.system("jarsigner -storepass %s %s %s" % (user_settings["keystore_pass"], fn, user_settings["keystore_name"]))
            # if system call returns with error, then return Status.FAILURE, regardless of --strict
        except:
            return Status.FAILURE if app_options["strict"] else Status.UNSUPPORTED

        return Status.SUCCESS
    
    def package(self):
        return Status.UNSUPPORTED
    def install(self):
        return Status.UNSUPPORTED

class Project:

    def __init__(self, filename):
        self.status = Status.UNSET

        self.filename = filename
        self.name = os.path.basename(os.path.abspath(filename))

        self.build_sys = None
        
        # Build system
        #if not self.build_sys:
        #    try:
        #        self.build_sys = arg_value("build-system")
        #    except NameError:
        #        pass

        if not self.build_sys:
            for fn in os.listdir("."):
                if os.path.isfile(fn):
                    fn_lower = fn.lower();
                    if fn_lower.endswith(".mf"):
                        self.build_sys = Java(self)
                        self.manifest = fn
                        # TODO: detect obfuscator from project
                    #elif fn_lower=="makefile":
                    #    self.build_sys = "make"
                    #    self.build_script = fn;
                    #elif fn_lower=="premake4.lua" or fn_lower=="premake.lua":
                    #    self.build_sys = "premake"
                    #    self.build_script = fn;
                    #elif fn_lower=="cmakelists.txt":
                    #    self.build_sys = "cmake"
                    #    self.build_script = fn;

        if not self.build_sys:
            # last ditch effort to detect build type by prevalence of filetypes
            pass

        # Project config
        for fn in os.listdir("."):
            if (fn.lower()=="sg.py" or fn.lower().endswith(".sg.py")) and os.path.isfile(os.path.join(os.getcwd(), fn)):
                with open(fn) as source:
                    # hackish name swap so we can use "name" in the project settings
                    self.name, self.build_sys.name = self.build_sys.name, self.name
                    eval(compile(source.read(), fn, 'exec'), {}, self.build_sys.__dict__)
                    self.name, self.build_sys.name = self.build_sys.name, self.name
                    

        if not self.build_sys:
            self.status = Status.UNSUPPORTED
            return

    def complete(self):
        print("Configuring %s..." % self.name)
        status = self.build_sys.configure()
        if status == Status.SUCCESS:
            print("Configured %s." % self.name)
        elif status == Status.FAILURE:
            return False

        print("Building %s..." % self.name)
        status = self.build_sys.make()
        if status == Status.SUCCESS:
            print("Built %s." % self.name)
        elif status == Status.FAILURE:
            return False

        print("Obfuscating %s..." % self.name)
        status = self.build_sys.obfuscate()
        if status == Status.SUCCESS:
            print("Obfuscated %s." % self.name)
        elif status == Status.FAILURE:
            return False

        print("Signing %s..." % self.name)
        status = self.build_sys.sign()
        if status == Status.SUCCESS:
            print("Signed %s." % self.name)
        elif status == Status.FAILURE:
            return False

        print("Packaging %s..." % self.name)
        status = self.build_sys.package()
        if status == Status.SUCCESS:
            print("Packaged %s." % self.name)
        elif status == Status.FAILURE:
            return False

        print("Installing %s..." % self.name)
        status = self.build_sys.install()
        if status == Status.SUCCESS:
            print("Installed %s." % self.name)
        elif status == Status.FAILURE:
            return False

        return True
       
def do_project(fn):
    project = Project(fn)

    if not project.status == Status.UNSUPPORTED:
        print "%s [%s]" % (project.name, project.build_sys)

    # only list details on list command
    if arg_command("list"):
        return 0

    if not project.status == Status.UNSUPPORTED:
        return 1 if project.complete() else -1

    return 0

def main():

    if arg_option("version"):
        splash()
        return
    if arg_anywhere("help") or arg_anywhere("?"):
        help()
        return

    wdir = os.getcwd();
    success_count = 0
    failed_count = 0

    r = do_project(".");
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
            r = do_project(fn);
            if r == 1:
                success_count += 1
            elif r == -1:
                failed_count += 1

            os.chdir(wdir)

    if not arg_command("list"):
        if failed_count:
            print("%s project(s) failed." % failed_count)
        else:
            print("%s project(s) completed." % success_count)

if __name__ == "__main__":
    main()

