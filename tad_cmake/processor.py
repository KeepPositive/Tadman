#! /usr/bin/python3

## Standard
import collections

""" This script takes the paired list returned by cmake_config_read and turns
it into a clean list of strings which can be utilized by a GUI.
"""

def cmake_message_filter(a_string):

    """ This function trims the beginning '// ' and the newline ('\n') from
    the end of the help message.

    This function returns a revised help message.
    """

    message = a_string[3:-1]

    return message

def cmake_option_name_filter(a_string):

    """ This function creates a title-like name for each option, out of the
    option itself.

    This function returns a title-like option name as a string.
    """

    option_name = (a_string.split(":"))[0]
    option_name = option_name.lower()
    option_name = option_name.replace('_', ' ')
    option_name = option_name.title()

    return option_name

def cmake_cli_option(a_string):

    """ This function removes the 'YES\n' or 'NO\n' from the end of the
    option so that it can be set differently later on.

    This function returns a revised option almost ready for CLI usage.
    """

    option = (a_string).split('=')
    option = "-D%s" % option[0]

    return option

def cmake_processor(a_list):

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

        option_title = cmake_option_name_filter(a_pair[1])
        help_message = cmake_message_filter(a_pair[0])
        option_flag = "%s=" % cmake_cli_option(a_pair[1])

        processed_dictionary[option_title] = [option_flag, help_message]

    return processed_dictionary
