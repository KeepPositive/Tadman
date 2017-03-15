=================================================
Tadman - *Some Package Manager Written in Python*
=================================================

.. note::

  The you wish to submit and issue or are looking to fork the repo for a pull
  please do so via the `Gitlab repo <https://gitlab.com/Tad-OS/Tadman>`_.
  The `GitHub repo <https://github.com/KeepPositive/Tadman>`_ is only a mirror.

What It Does
++++++++++++

Tadman acts as a graphical wrapper for common build systems and makes
configuring and building source code easily. It then (by default) installs
the built package in ``/usr/local/tadman/PACKAGE-NAME`` and symlinks the
files to your root directory where they belong, similiar to GNU Stow.
Uninstalling an old program is as easy as running a single command:

::

  $ sudo tadman-curses uninstall PACKAGE

What It Does Not Do
+++++++++++++++++++

A flaw that one may note is Tadman's lack of dependency tracking; This is an
intentional design choice. While it may not be the fastest approach, Tadman
does not wish to make choices for the user like a majority of other package
managers.

With Tadman, there are no package maintainers or unnecessary dependencies.
Rather, it gives the user direct access to the world's largest and most
up-to-date software library: the internet. It allows users to install
software from a Git repo and uninstall it easily. All you need to do is find
some source code, and install it using a single command:

::

  $ sudo tadman-curses build PATH

Dependencies
++++++++++++

The only necessary dependencies for Tadman are:

* python3 (built with curses support)
* Setuptools module for python3

Though, there are several optional dependencies:

* asciidoctor (to generate the manual page)
* CMake (to build CMake-based projects)
* pygobject and GTK+3 (to use the GTK+ 3 interface)
* pytest (to run some tests)

Installation
++++++++++++

Tadman can be installed using Git and Setuptools using the following commands
on a GNU/Linux system:

::

  $ git clone https://github.com/KeepPositive/Tadman.git
  $ cd Tadman
  $ python3 setup.py install

.. note::

  Currently, use of the ``--user`` flag does not work since Tadman requires
  root access for its installation.

You should now have an executable named ``tadman-curses`` in your path.

Usage
+++++

Tadman should make building source code packages easier. Try it out by
downloading some source code that uses autotools or CMake, and then run the
following:

::

  $ python3 tadman-curses build [PATH]

A curses-based GUI will open, and prompt you for the package name and version
(necessary for better book-keeping of the installation). Next, an options list
will appear, where you can check off the options you want, or leave the ones
you don't blank. Once you are ready, hit 'e', and assuming you have all of
the dependencies your program requires, the program will be installed.

For a complete list of available arguments, check out
`the manpage <docs/tadman.man.adoc>`_.

Licensing
+++++++++

Copyright © 2016 Ted Moseley. Free use of this software is granted under the
terms of the `MIT Open Source License <https://opensource.org/licenses/MIT>`_.
