===============
 tadman-curses
===============

---------------------------------------------
generate unix manpages from reStructured text
---------------------------------------------

:Author: tmoseley1106@gmail.com
:Date:   2017-03-15
:Copyright: public domain
:Version: 0.1.3
:Manual section: 8
:Manual group: Package Management

SYNOPSIS
========

tadman-curses COMMAND [PATH]

DESCRIPTION
===========

Tadman is a portable package manager which can run on any GNU/Linux based
operating system. It is written in pure python3 and possesses very few
dependencies.

The idea is that Tadman acts as a wrapper for popular build systems.
Currently, Tadman is able to build GNU Autotools and CMake based projects.
It then installs the compiled source code into the ``/usr/local/tadman``
directory. Here, packages are placed within their own folders. The
contents of these folders are then linked to the ``/usr/bin`` through a
system of symlinks.

Similarly, Tadman can uninstall packages by removing all symlinks.

COMMANDS
========

``build <PATH>``
  Run the standard build process, including entering package info and choosing
  options. Then prompt for an installation.

``help``
  Print this help message and exit.

``install <NAME | PATH>``
  Link files in a package's install directory to root.

``list [NAME]``
  If no argument is passes, list will provide all of the built packages with
  the package directory (/usr/local/tadman by default). If a name is passed,
  all of the files installed for NAME will be printed.

``uninstall <NAME | PATH>``
  Unlink files from root directories.

``version``
  Print a version string and exit.

EXAMPLES
========

Build
+++++

Let's say you want to install a program using Tadman named 'foo' and it is
version '1.2.3'. The folder containing the source code is likely named
'foo-1.2.3'. So we will build it and install it using this command:

::

  tadman-curses build /path/to/foo-1.2.3

Simply follow the prompts, choose your options, and the build process will
begin.

Uninstall
+++++++++

Now, let's say that 'foo-1.2.4' is released a month later. You will want to
uninstall the 'foo-1.2.3' package. Just run this command:

::

  tadman-curses uninstall foo-1.2.3

The symlinks hold the program in place will be broken, and you can now build
and install foo-1.2.4 just like we did previous.

Reinstall
+++++++++

As one last example, let's say there is a bug in 'foo-1.2.4', and you still
have foo-1.2.3 in your '/usr/local/tadman' directory. You can uninstall
'foo-1.2.4', and reinstall 'foo-1.2.3' using two commands:

::

  tadman-curses uninstall foo-1.2.4
  tadman-curses install foo-1.2.3

.. note::

  All of these commands must be run as the root user. If you are not the
  root user, Tadman will display an error message.

COPYING
=======

Copyright © 2016 Ted Moseley. Free use of this software is granted under
the terms of the MIT Open Source License <https://opensource.org/licenses/MIT>.
