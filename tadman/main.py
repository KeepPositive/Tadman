""" This script includes a bunch of functions used by the scripts in the bin/
directory, like tadman-curses.
"""

# Standard
import os
import subprocess
import sys
# Scripts
from tadman import autotools, cmake, path_tools

def simple_prompt(a_string):

    """ This function simple prompts the user with a standard string
    and yes or no input.
    """

    prompt = "%s [y,N] " % a_string
    choice = input(prompt)

    if choice in ['n', 'N', '']:
        return False
    elif choice in ['y', 'Y']:
        return True

def check_for_root():

    """ Simply check whether the user running the script is the root
    user. If not, end the script prematurely and throw an error message.
    """

    if os.geteuid() != 0:
        print("Only root can execute this command")
        sys.exit(1)

def list_package_directory(a_path):

    """ This function is mostly self explanitory. It prints out the
    names of built package in the user's package directory.
    """

    directory_contents_list = sorted(os.listdir(a_path), key=str.lower)

    for subpath in directory_contents_list:
        full_subpath = os.path.join(a_path, subpath)
        if os.path.isdir(full_subpath):
            print(subpath)

def list_package_contents(root_path, a_path):

    """ This function is a simplified version of the sym_farm
    function. It lists where all of the files would be installed,
    IF this package were to be installed. It currently has no way of
    verifying if this is true or not as of right now.
    """

    package_dir = find_link_path(root_path, a_path)
    remove_length = len(package_dir)
    for root, _, files in os.walk(package_dir):

        for name in files:

            rel_path = os.path.join(root, name)
            new_path = rel_path[remove_length:]

            print(new_path)

def find_build_type(a_path):

    """ One can often find what build system is used by looking at the
    files present in the main folder. This function does it
    automagically and returns which build system it believes is used.
    """

    if os.path.isfile("%s/configure" % a_path):
        build_type = 'autotools'
    elif os.path.isfile("%s/CMakeLists.txt" % a_path):
        build_type = 'cmake'
    elif os.path.isfile("%s/autogen.sh" % a_path):
        build_type = 'autogen'

    return build_type

def get_package_info(a_path):

    """ This function determines which build system is used by viewing
    the files available in the root of a source code directory. It
    runs the name_version_split function, which returns a believed
    package name and package version straigh from the source folder's
    name.
    """

    # Get the name and version from the basename of the source path
    package_name, package_version = path_tools.name_version_split(a_path)

    # Find out which build system is available
    build_type = find_build_type(a_path)
    # Get the available options based on what build system is found
    if build_type == 'autotools':
        option_list, install_list = autotools.get_config_lists(a_path)
        option_dict = autotools.option_processor(option_list)
        install_dict = autotools.install_flag_processor(install_list)
    elif build_type == 'cmake':
        option_list, install_list = cmake.get_options_list(a_path)
        option_dict = cmake.option_processor(option_list)
        install_dict = cmake.install_flag_processor(install_list)

    return option_dict, install_dict, package_name, package_version, build_type

def configure_maker2(mode, install_list, option_list):

    command_list = []

    if mode == 'autotools':
        command_list.append('./configure')
        command_list.append('--prefix=/usr')

    elif mode == 'cmake':
        command_list.append('cmake')
        command_list.append('-DCMAKE_INSTALL_PREFIX=/usr')

    for install_flag in install_list:
        command_list.append(install_flag)

    for option_flag in option_list:
        command_list.append(option_flag)

    return command_list

def build_package_source(a_path, output_directory, configure_command):

    """ This function runs some simple commands in order to configure
    and build source code. It also installs in to the user's package
    directory. How nice.
    """

    # Change to the directory
    os.chdir(a_path)
    # Run the configuration command with options
    subprocess.run(configure_command)
    # Build the sources
    build = subprocess.run(['make', '-j', '4'])
    # Install it in the Tadman directory
    install = subprocess.run(['make', "DESTDIR=%s" % output_directory, 'install'])

    if build.returncode == 0 and install.returncode == 0:
        return True
    else:
        return False

def find_link_path(root_dir, name_or_path):

    """ When installing and uninstall packages using Tadman, the user
    is allowed to pass in an absolute path to the package, or just
    it's name. This is the function that decides what the input is,
    and returns the desire path.
    """

    link_path = ()
    root_path = root_dir

    if os.path.isdir(name_or_path):
        if root_path in name_or_path:
            link_path = name_or_path
        else:
            print("Not a package")
    else:
        name_path = "%s/%s" % (root_path, name_or_path)
        if os.path.isdir(name_path):
            link_path = name_path
        else:
            print("Directory entered does not exist")
            return ''

    return link_path

def print_help_message():

    """ This function prints a help message. Enough said."""

    help_list = ["Usage: tadman [ARGUMENT] [...]\n",
                 "Arguments:",
                 "  build\t\tBuild a package from source code and install it",
                 "  help\t\tPrint this help message and exit",
                 "  install\tCreate symlinks for a built package",
                 "  list\t\tList all built software packages",
                 "  uninstall\tDestroy all symlinks for a package",
                 "  version\tPrint version info and exit\n",
                 "Copyright © 2016 Ted Moseley.\n",
                 "Free use of this software is granted under the terms of the",
                 "MIT License available at <https://opensource.org/licenses/MIT>."]

    help_string = ''

    for a_string in help_list:
        help_string += '%s\n' % a_string

    print(help_string, end='')
