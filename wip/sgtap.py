#!/usr/bin/python2
"""
Siege-Tools SiegeTap (\"sgtap\")
Template-based file creation and project generator
http://github.com/flipcoder/siege-tools
Version 0.2.0
Copyright (c) 2012 Grady O'Connell

File and project creation:
    sgtap myfile -> makes blank file called "myfile" since its name doesnt have extension
    sgtap file.cpp -> makes file "file.cpp" according to .cpp filetype and context (blank if no template found)
    sgtap blah@make -> makes a makefile project "blah" (plug-in doesn't need extension)
    sgtap blah.h -> makes c OR c++ header file (plug-in will look for cpp or c files for context hints)
    sgtap blah@java -> makes a java project named "blah"
    sgtap blah@cpp -> make a C++ project named "blah"
    sgtap blah@cpp.git.premake -> c++ git project w/ premake build system

Opening files after creation (works even if they exist already)
    sgtap -e file.txt
"""

import os
import sys
from common import *
from common import Args

def splash():
    print __doc__.replace("sgtap",program_name()).strip()

def commands():
    print("Options: %s" % ", ".join(Args.valid_options))
    print("Keys: %s" % ", ".join(Args.valid_keys))

def help():
    splash()
    print
    commands()

class Template(object):
    def __init__(self, fn):
        pass
    @staticmethod
    def from_type(fn):
        pass

class Project:
    def __init__(self, fn, global_args):
        self.fn = fn
        self.type = None
        if not self.fn:
            raise IOError()
        self.global_args = global_args

        # get defaults or custom (user-provided) separator and switch chars
        sep_list = [global_args.value("separator-char")] if global_args.value("separator-char") else ['@', ':', ';']
        switch_list = [global_args.value("switch-char")] if global_args.value("switch-char") else ['+']

        # filename/type separators
        tokens = None # scope
        for sep in sep_list:
            tokens = self.fn.split(sep)
            token_count = len(tokens)
            if token_count == 2:
                self.fn = tokens[0]
                self.type = tokens[1]
                break
            tokens = None
        if not tokens:
            tokens = [self.fn]
        
        # get extension (even if unused)
        self.ext = None
        tokens = self.fn.split('.')
        if len(tokens) > 1:
            self.fn = tokens[0] # new filename (without ext)
            self.ext = '.'.join(tokens[1:]) # use everything past first dot, ex: tar.gz
            if not self.type:
                self.type = self.ext

        # get switches for typed projects (when type is explicitly stated)
        # FIXME if necessary:
        #   this only allows switches to be used on projects where a type is specified (not infered from extension)
        # this may require a better parser if fixed
        self.switches = None
        if self.type:
            for switch in switch_list:
                tokens = self.type.split(switch)
                if len(tokens) > 1:
                    self.type = tokens[0]
                    #self.switches = tokens[1:]
                    break # correct switch char found

        # check if filename and template exist (if so, "touch" (update date of) the file)
        self._locate()

        if self.global_args.option("verbose") or self.global_args.option("list"):
            print "Filename: %s%s" % (self.fn, " (already exists)" if self.exists else "")
            if self.type:
                print "- Template: %s" % self.type
            if self.switches:
                print "- Switches: %s" % ','.join(self.switches)
            if self.ext:
                print "- Extension: %s" % self.ext
            if self.exists:
                print "- Exists: %s" % self.exists

        if not self.global_args.option("list"):
            self._process()

    def __str__(self):
        return self.fn

    def _process(self):
        verbose = Args.option("verbose")

    def _locate(self):
        self.exists = False
        self.template_path = None
        if not self.fn:
            raise IOError("Must provide a filename.")

        t = Template.from_type(self.type)
        if not t:
            raise IOError("No template matching '%s'" % self.type)
        #if not self.type:
        #    pass # normal file?
        # TODO template not found error
        # TODO warnings when directory is given extension
        # TODO warnings when extensions mismatch with plug-in suggested extensions

def error(e):
    print >> sys.stderr, "%s: %s" % (program_name(), e)
    print >> sys.stderr, "Try '%s --help' for more information." % program_name()

def main():
    # interactive lets you check each flag for the plug-in while projects are being built
    Args.valid_options = ["?", "help", "interactive", "warn", "verbose", "edit", "replace", "remove", "force", "list"]
    Args.valid_keys = ["separator-char", "switch-char", "type-default", "switch-default", "title"] # --ignore=context
    Args.process()

    set_program_name(Args.value("title"))

    if Args.option("help") or Args.option("?"):
        help()
        return

    # check for bad options (not yet implemented)
    for bad in ("interactive", "warn", "open", "replace", "remove", "force"):
        if Args.option(bad):
            error("option '%s' not yet implemented" % bad)
            return
    
    # loop through provided filenames
    if Args.filenames:
        for fn in Args.filenames:
            try:
                t = Project(fn, Args)
            except Exception as e:
                error(e)
            #except Exception as e:
            #    return
            # if t:
    else:
        error("missing file operand" % program_name())
        return

if __name__=="__main__":
    main()

