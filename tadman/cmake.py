""" Welcome to Tadman's CMake script
"""

# Standard
import collections
import os
import subprocess

def remove_empty_folders(path):

    """ This method removes everything within a directory. Great stuff.

    Credit for this method goes to Jacob Tomlinson. Thanks!
    Check it out his website at: https://www.jacobtomlinson.co.uk
    """

    if not os.path.isdir(path):
        return

    # Remove empty subfolders
    files = os.listdir(path)
    if len(files):
        for a_file in files:
            full_path = os.path.join(path, a_file)
            if os.path.isdir(full_path):
                remove_empty_folders(full_path)


def get_options_list(a_path):

    """ This function runs the CMake command (which unlike Autotools,
    CMake runs the configure process before it can print the help
    options) and then sends the useful options into the 'config_out.txt'
    file. In order to do this, a build directory (called 'tadman_build').
    If this folder already exists, it is emptied first.
    """

    cmake_cache_path = "%s/CMakeCache.txt" % a_path
    cmake_build_dir = "%s/tadman_build" % a_path

    if not os.path.isfile(cmake_cache_path):
        # If the tadman_build directory exists, remove it
        if not os.path.isdir(cmake_build_dir):
            # Create the tadman_build dir
            os.mkdir(cmake_build_dir)
        else:
            remove_empty_folders(cmake_build_dir)
        # Change to the directory so files will be stored there
        os.chdir(cmake_build_dir)
        subprocess.run(['cmake', a_path])

    cache_list = []
    option_list = []

    cache_file = open(cmake_cache_path, 'r')

    for a_line in cache_file:
        cache_list.append(a_line)

    cache_lines = len(cache_list)

    for index in range(cache_lines - 1):
        a_line = cache_list[index]
        if 'BOOL=ON' in a_line or 'BOOL=OFF' in a_line:
            message_line = cache_list[index - 1]
            option_list.append([message_line[:-1], a_line[:-1]])

    return option_list

def get_option_title(a_string):

    """ This function creates a title-like name for each option, out of the
    option itself.

    This function returns a title-like option name as a string.
    """

    option_name = (a_string.split(":"))[0]
    option_name = option_name.lower()
    option_name = option_name.replace('_', ' ')
    option_name = option_name.title()

    return option_name

def get_clean_cli_option(a_string):

    """ This function removes the 'YES\n' or 'NO\n' from the end of the
    option so that it can be set differently later on.

    This function returns a revised option almost ready for CLI usage.
    """

    option = (a_string).split('=')
    option = "-D%s" % option[0]

    return option

def option_processor(a_list):

    """ This is almost like the main function of this script. It pretty much
    just runs all of the functions from above to create a pretty, formatted
    list of options for a GUI to use.

    This function returns a processed list of options, with each item
    formatted as:

        [title, cli_option, help_message]

    Note: the cli_option still needs a 'YES' or 'NO' appended to end for it
    to work properly.
    """

    processed_dictionary = collections.OrderedDict()

    for a_pair in a_list:

        option_title = get_option_title(a_pair[1])
        help_message = a_pair[0].lstrip('// ')
        option_flag = "%s=" % get_clean_cli_option(a_pair[1])

        processed_dictionary[option_title] = [option_flag, help_message]

    return processed_dictionary
