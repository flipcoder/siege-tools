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

sgmake is a build automation system.  It's job is to intelligently select and run the specific steps required by common build systems by analyzing the given directories (usually just the current directory), figuring out which build system was intended for the projects found, and attempting to build the projects.  It takes into account limitations of the current platform, the project, and those rules set up by the user through config files.  Build systems can chose to add other steps needed as they're detected, and/or reorder them as needed.
If no build system is found, it can look at the filetypes and even analyze the source files to see if the project can still be built.

The goal of Sgmake is to build most source-based projects out of the box, without difficulty.
This allows for projects to pull and build dependencies from any
source-based project easily, without having to support the same build systems.

Detector plug-ins run first, and provide information about each project to the other plug-ins, such as the count and percentages of certain filetypes, and other clues about the project environment.
These clues inform later plug-ins of how to build the provided package.

Each step of the build process has its own set of plug-ins.  The plug-in types
are detect, analyze, clean, preprocess, make, obfuscate, doc, sign, package, install, test, and deploy.
These plug-ins work together as a decision-tree to build a project completely.
Look below at the feature list to see a list of the plug-ins supported.

#### What is Supported ####

- Automatic cleaning and rebuild
- Premake projects
- CMake projects
- Source-only Java projects with manifest files
- Make-based projects
- Qt qmake
- Node.js npm packages
- Bower packages
- Docker dockerfiles
- Grunt (Javascript Task Runner)
- Allatori obfuscation
- Java Jar Signing
- IZPack installer packaging
- NSIS Installers (using Wine on non-windows platforms) (very early proof-of-concept, but it "works")
- Multi-threaded make (auto-adds -j based on # cores)
- RAM-based compilation (WIP, auto-relinking of tmpfs-mounted obj folder)

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

Then, to build a project from a file inside a project dir, just type in vim:

    :make

Or async version (using [AsyncCommand](https://github.com/pydave/AsyncCommand/))

    :AsyncMake

And to bring up the quicklist, type:

    :copen

Eventually, siege-tools event plug-ins will allow you to jump into vim from the
command at the context of the first error.  I haven't written this part yet though. :)

##### Calling from Vim (alternative to above) #####

In your .vimrc add a line like this (assuming siege-tools is in your home dir's bin and <leader>s is your choice for sgmake key):

    nnoremap <leader>s :w<cr>:!sgmake -R %:p:h<cr>

When leader+s is pressed, sgmake does a backwards scan (-R option) for projects starting from the file you're editing, assuming you're probably editing in either the project or a nested source dir, and then runs the build on the first project it detects using the build system detected.

An async alternative to the above using [vim-dispatch](https://github.com/tpope/vim-dispatch/):

    " (S)gmake (build) the associated project
    nmap <leader>s :w<cr>:Dispatch! sgmake -Rd<cr>

You may also want to run the application once the build finishes:

    " (R)un the associated program using sgrun
    nmap <leader>r :w<cr>:Dispatch! sgrun<cr>

###sgrun (SiegeRun)###

Ever tried to simply run a program while editing its code in a deep nested
directory?  SiegeRun digs deep, attempts to figure out which binary you intended to run, and runs it.

Example:

Let's say your working dir is MyProject/src/video and you're editing Canvas.cpp

A 'sgrun' call, will find and run: "MyProject/bin/mybinary" w/
"MyProject/bin/" as the working directory

It also intelligently tries to avoid supplemental scripts and tests, if there is something better to run.

SiegeRun also forwards your parameters to the target, but looks for special "---"-prefixed flags to invokve
special behavior.  One such switch is "---e" which can filters targets using a regex expression.

SiegeRun also supports Node.js package.json files as target hints.

## Future ##

- JSON-based dependencies, with system package managers and git-based providers
- Installer
- Improved documentation
- Improved error handling

- SiegeTap (sgtap)
    - Alternative to Unix "touch" but with basic project templates
    - Generating template projects to use with sgmake or your build system of choice
    - Context-aware file and project templates and generators

## Contributing ##
If you find this project useful, consider contributing or spreading the word to other developers.
Once the addon system is done, I could use contributors to write addon steps for different languages and build systems.

## Contact ##
Contact me at flipcoder@gmail.com for questions, comments, etc.

