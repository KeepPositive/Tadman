""" Welcome to Tadman's CMake script"""

# Standard
import collections
import os
import subprocess
# Scripts
import tadman.path_tools

def get_options_list(a_path):

    """ This function runs the CMake command (which unlike Autotools,
    CMake runs the configure process before it can print the help
    options) and then sends the useful options into the 'config_out.txt'
    file. In order to do this, a build directory (called 'tadman_build').
    If this folder already exists, it is emptied first.
    """

    cmake_cache_path = "%s/tadman_build/CMakeCache.txt" % a_path
    cmake_build_dir = "%s/tadman_build" % a_path

    if not os.path.isfile(cmake_cache_path):
        # If the tadman_build directory exists, remove it
        if not os.path.isdir(cmake_build_dir):
            # Create the tadman_build dir
            os.mkdir(cmake_build_dir)
        else:
            tadman.path_tools.remove_empty_folders(cmake_build_dir)
        # Change to the directory so files will be stored there
        os.chdir(cmake_build_dir)
        subprocess.run(['cmake', a_path])

    cache_list = []
    option_list = []
    install_list = []

    cache_file = open(cmake_cache_path, 'r')

    for a_line in cache_file:
        cache_list.append(a_line)

    cache_lines = len(cache_list)

    for index in range(cache_lines - 1):
        a_line = cache_list[index]

        for indicator in [':BOOL=', ':PATH=']:
            if indicator in a_line:
                if cache_list[index - 1][2] == ' ':
                    line_one = cache_list[index - 2][:-1]
                    line_two = cache_list[index - 1][:-1]
                    message_line = "{}{}".format(line_one, line_two[2:])
                else:
                    message_line = cache_list[index - 1][:-1]

                if 'BOOL=ON' in a_line or 'BOOL=OFF' in a_line:
                    option_list.append([message_line, a_line])
                elif ':PATH' in a_line:
                    install_list.append([message_line, a_line])

    return option_list, install_list

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

def get_clean_bool_option(a_string):

    """ This function removes the 'YES\n' or 'NO\n' from the end of the
    option so that it can be set differently later on.

    This function returns a revised option almost ready for CLI usage.
    """

    option, _ = (a_string).split('=')
    option = "-D{}".format(option)

    return option

def get_clean_path_option(a_string):
    """ Typically install flags are shown as 'flag:PATH=value', so
    function splits the two, and removes the :PATH portion.

    This function returns a tuple consisting of the install flag and
    the default value that is set for it.
    """
    option, default = a_string.split('=')
    option = option[:-5]

    return option, default

def option_processor(a_list):

    """ This is almost like the main function of this script. It pretty much
    just runs all of the functions from above to create a pretty, formatted
    list of options for a GUI to use.

    This function returns a processed list of options, with each item
    formatted as:

        title: [cli_option, help_message]

    Note: the cli_option still needs a 'YES' or 'NO' appended to end for it
    to work properly.
    """

    processed_dictionary = collections.OrderedDict()

    for a_pair in a_list:

        option_title = get_option_title(a_pair[1])
        if option_title[:5] == 'Cmake':
            option_title = option_title[6:]

        help_message = a_pair[0].lstrip('//')
        option_flag = "%s=" % get_clean_bool_option(a_pair[1])

        processed_dictionary[option_title] = [option_flag, help_message]

    return processed_dictionary

def install_flag_processor(a_list):

    """ This function deals with turning the install flag options into
    a nicely formatted dictionary. This requires modifying the
    raw_flag, but it is easily changed back later on after the user
    enters information using the GUI.

    This function returns a dictionary with the contents in the format
    of:

        modified_flag: [description, default_value]

    """
    processed_dictionary = collections.OrderedDict()

    for a_pair in a_list:

        install_title, default_path = get_clean_path_option(a_pair[1])

        if install_title == 'CMAKE_INSTALL_PREFIX':
            continue

        description = a_pair[0].lstrip('//')

        processed_dictionary[install_title] = [description, default_path]

    return processed_dictionary
