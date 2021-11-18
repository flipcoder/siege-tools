"""
Context-based error handling
This event plug-in will put the user into whatever file caused the error during the build process,
using either their prefered editor or by giving the information back to the program
that called sgmake (editor or editor plug-in)

It is enabled based on a combination of:
    what environment the user ran the program in
    what editor the user has set to their default in sgrc
"""


# TODO: if event plug-in enabled by user's environment settings,
# do check if $EDITOR == vim,  vim -c make! -c cwindow (?)
