# Tadman
_Some Package Manager Written in Python_

This is a (universal?) package manager that is currently in developement. It is being designed to act as wrapper for basic commands like the autotools build process and CMake. It will also be written in (_hopefully_) pure python, and have very few dependencies.


### Dependencies

The only dependencies so far are:
+ Python 3 (_obviously_)
+ click, a Python CLI module (You can find it [here](http://click.pocoo.org/6/).)

Some optional dependencies are:
+ CMake, to build CMake projects (You can find it [here](https://cmake.org/).)

### Execution

Tadman should make building from source code easier. Right now, there is no system in place to build a Tadman executable or even install the scripts. Until then, you can test it by running the following:

    $ git clone https://github.com/KeepPositive/Tadman.git
    $ cd Tadman
    $ python3 tadman_main.py [PATH_TO_SOURCE_CODE]'

It _should_ print out some small lists of the configure options available for the program you wish to install. A way to edit these options and run the configure script is coming soon. 
