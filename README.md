![siege-tools](https://raw.githubusercontent.com/flipcoder/siege-tools/14b4912238590352658221b1e85d376dd5c660d7/sgtools.png)

http://github.com/flipcoder/siege-tools

Copyright &copy; 2012 Grady O'Connell

See LICENSE for more information

=======================================

## Purpose ##
Siege Tools is a plugin-based build automation toolset.

Currently, the only tools ready for use is SiegeMake (sgmake) and SiegeRun (sgrun).

## Components ##

###sgmake (SiegeMake)###

sgmake is a build system auto-detector / wrapper.  It's job is to select and run the specific steps required by common build systems by analyzing the given directories (usually just the current directory), figuring out which build system was intended for the projects found, and attempting to build the projects.  It takes into account limitations of the current platform, the project, and those rules set up by the user through config files.  Build systems can chose to add other steps needed as they're detected, and/or reorder them as needed.  If no build system is found, it can look at the filetypes and even analyze the source files to see if the project can still be built.

Detector plug-ins run first, and provide information about each project to the other plug-ins, such as the count and percentages of certain filetypes, and other clues about the project environment.

Each step of the build process has its own set of plug-ins.  The plug-in types are detect, analyze, clean, preprocess, make, obfuscate, doc, sign, package, install, test, and deploy.
Look below at the feature list to see a list of the plug-ins supported.

Since sgmake is still a work-in-progress, "Action" plug-ins are not yet implemented.  Actions are what allows sgmake to send information from within the build process back to the calling environment.
An example of this would be if a user runs sgmake from within Vim, the build process can send back errors back or trigger custom notification plug-ins, such as launching a debugger.  These events happen only if the environment supports them, such as OS-specific pop-up notifications), much like the build plug-ins.

#### What is Supported ####

- Automatic cleaning and rebuild
- Premake projects
- CMake projects
- Source-only Java projects with manifest files
- Make-based projects (minimal support right now)
- Qt qmake
- Node.js npm packages
- Bower packages
- Docker dockerfiles
- Grunt (Javascript Task Runner)
- Allatori obfuscation
- Java Jar Signing
- IZPack installer packaging
- NSIS Installers (using Wine on non-windows platforms) (very early proof-of-concept, but it "works")
- Take a look in the steps/ and events/ folder to see some progress on new plug-ins I've started.  Some of these are currently disabled.

#### Basic Usage ####

This example assumes you're using Linux, but MacOS should work similarly.

There's no installer right now, so simply create an alias using your shell to call the sgmake.py file when you type "sgmake",
This is the best bet so you can keep the git repo current as I change things.
Example:

    alias sgmake="/usr/bin/env python2 ~/bin/siege-tools/sgmake.py"

Or, make a new file /usr/bin/sgmake, with contents:

    #!/bin/bash
    /usr/bin/env/python2 ~/bin/siege-tools/sgmake.py "$@"

(Use your own path to siege-tools)

Then, give it execute permissions:

    sudo chmod +x /usr/bin/sgmake

To detect and build a sgmake project do:

    sgmake

To build a batch of sgmake projects recursively:

    sgmake -r

To build a project from a nested directory inside a project (such as in a src/ folder:

    sgmake -R

To list the projects detected in a directory

    sgmake -l

To list projects recursively:

    sgmake -lr

#### Vim Integration ####

##### Setting sgmake as vim's "makeprg" #####

Add this to .vimrc

    let makeprg=sgmake\ -R

Then, to build a project from a file inside a project dir, just type in vim;

    :make

And to bring up the quicklist, type:

    :copen

Eventually, siege-tools event plug-ins will allow you to jump into vim from the
command at the context of the first error.  I haven't written this part yet though. :)

##### Calling from Vim (alternative to above) #####

In your .vimrc add a line like this (assuming siege-tools is in your home dir's bin and <leader>s is your choice for sgmake key):

    nnoremap <leader>s :!/usr/bin/env python2 ~/bin/siege-tools/sgmake.py -R %:p:h<cr>

When leader+s is pressed, sgmake does a backwards scan (-R option) for projects starting from the file you're editing, assuming you're probably editing in either the project or a nested source dir, and then runs the build on the first project it detects using the build system detected.

###sgrun (SiegeRun)###

Ever tried to simply run a program while editing its code in a deep nested
directory?  SiegeRun digs deep, finds the binary, and runs it for you.

Example:

Let's say your working dir is MyProject/src/video and you're editing Canvas.cpp

A 'sgrun' call, will find and run: "MyProject/bin/mybinary" w/
"MyProject/bin/" as the working directory

It also intelligently tries to avoid supplemental scripts and tests.

## Future ##

- Installer
- Improved documentation

- SiegeTap (sgtap)
    - Alternative to Unix "touch" but with basic project templates
    - Generating template projects to use with sgmake or your build system of choice
    - Context-aware file and project templates and generators

- SiegeMod (sgmod)
    - a state machine of build switches for your project
    - manipulate source code abstract syntax trees from an external script similar to jquery's manipulation of DOM
    - does not require embedding incompatible code like other preprocessors
    - compatible with sgmake (above)

## Contributing ##
If you find this project useful, consider contributing or spreading the word to other developers.
Once the addon system is done, I could use contributors to write addon steps for different languages and build systems.

## Contact ##
Contact me at flipcoder@gmail.com for questions, comments, etc.

