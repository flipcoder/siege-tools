# siege-tools
http://github.com/flipcoder/siege-tools

Copyright &copy; 2012 Grady O'Connell

See LICENSE for more information

=======================================

## Purpose ##
Siege Tools is a collection of cross-platform CLI developer tools designed to bring more IDE-like functionality back to the command line.
It attempts to solve common tedious tasks involved with programming in a way that works with multiple platforms and languages.

## Components ##

- SiegeMake (sgmake)
    - a multi-language, extensible build system
    - a wrapper for projects using other build systems
    - an automatic build system detector and autoconfigurer
    - a wrapper around current systems (make, cmake, premake, etc.)
    - a cross-platform dependency resolver (eventually)
    - supports more advanced build steps such as obfuscation and digital signing

## Future ##

- SiegeMod (sgmod)
    - a multi-language, extensible preprocessor
    - compatible with sgmake (above)
    - a state machine of custom switches for your project
    - does not require embedding incompatible code like other preprocessors
    - manipulate source code from an external script similar to manipulating DOM

- Vim plugins for each tool

## Contributing ##
If you find this project useful, consider contributing or spreading the word to other developers.
Once the addon system is done, I could use contributors to write addon steps for different languages and build systems.
My primary plan is to implement my most familiar languages first (C/C++(+ autotools/make/cmake/premake/scons), Java(+ ant/maven), Vala), and move on from there.

## Contact ##
Contact me at flipcoder@gmail.com for questions, comments, etc.

