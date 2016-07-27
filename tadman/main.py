""" This script includes a bunch of functions used by the scripts in the bin/
directory, like tadman-curses.
"""

# Standard
import os
import subprocess
import sys
# Scripts
from tadman import autotools, cmake, logger, path_tools

def simple_prompt(a_string):
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
    directory_contents_list = sorted(os.listdir(a_path), key=str.lower)

    for subpath in directory_contents_list:
        full_subpath = os.path.join(a_path, subpath)
        if os.path.isdir(full_subpath):
            print(subpath)

def list_package_contents(root_path, a_path):
    package_dir = find_link_path(root_path, a_path)
    remove_length = len(package_dir)
    for root, dirs, files in os.walk(package_dir):

        for name in files:

            rel_path = os.path.join(root, name)
            abs_path = os.path.abspath(rel_path)
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
    # Get the name and version from the basename of the source path
    package_name, package_version = path_tools.name_version_split(a_path)

    # Find out which build system is available
    build_type = find_build_type(a_path)
    # Get the available options based on what build system is found
    if build_type == 'autotools':
        raw_list = autotools.get_options_list(a_path)
        clean_dict = autotools.option_processor(raw_list)
    elif build_type == 'cmake':
        raw_list = cmake.get_options_list(a_path)
        clean_dict = cmake.option_processor(raw_list)

    return clean_dict, package_name, package_version, build_type

def configure_maker(in_dict, in_list, mode):

    configure_indexes = in_list
    configure_list = []
    option_list = []

    for item in in_dict:
        configure_list.append(item)

    if mode == 'autotools':
        option_list.append('./configure')
        option_list.append('--prefix=/usr')

    elif mode == 'cmake':
        option_list.append('cmake')
        option_list.append('-DCMAKE_INSTALL_PREFIX=/usr')

    for index in configure_indexes:
        option = in_dict[configure_list[index]][0]

        if mode == 'cmake':
            option = "%s%s" % (option, 'ON')

        option_list.append(option)

    return option_list

def build_package_source(a_path, output_directory, configure_command):
    # Change to the directory
    os.chdir(a_path)
    # Run the configuration command with options
    subprocess.run(configure_command)
    # Build the sources
    subprocess.run(['make', '-j', '4'])
    # Install it in the Tadman directory
    subprocess.run(['make', "DESTDIR=%s" % output_directory, 'install'])

def find_link_path(root_dir, name_or_path):

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

    arg_dict = {'build': "Build a package from source and install",
                'help': "Print this help message and exit",
                'install': "Create symlinks for a built package",
                'list': "List all built software packages",
                'uninstall': "Destroy all symlinks for a package",
                'version': "Print version info and exit"}

    print("Usage: tadman [ARGUMENT] [...]\n\nArguments:")

    for argument in sorted(arg_dict):
        print("    %s\t%s" % (argument, arg_dict[argument]))
