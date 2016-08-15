""" This script includes all of the functions necessary to handle a
build using GNU Autotools. It generally runs the configure script,
find the available options, and then processes them into a dictionary
for use by a GUI frontend.
"""

# Standard
import collections
import subprocess

def autotool_filter(a_string):

    """ This function simply removes the '--' before each option and the
    newline character ('\n') from each string, and then splits the option
    from the message at the first space it sees.

    This function returns a pair consisting of a raw option, and a raw
    message which will be cleaned up later.
    """

    filtered_pair = a_string[2:].split(' ', 1)

    if len(filtered_pair) > 1:
        filtered_pair[1] = filtered_pair[1].lstrip()

    return filtered_pair

def find_first(search_list, phrase):

    """ This function looks for the first occurence of a string in a
    list. The search will only find a direct match to the string
    passed in as 'phrase'. Note that if the list is made up of raw
    text taken from a terminal or something of the sort, you may need
    to add a newline character (i.e. '\n') to the end of your 'phrase'.

    This function returns the line number of the first occurence without any
    padding (So if zero is returned, the phrase was found on line one of the
    file).
    """

    found_occurance = ()

    for a_line in range(0, len(search_list)):

        if search_list[a_line] == phrase:
            found_occurance = a_line
            break

    return found_occurance

def get_config_lists(path):

    """ This function runs the configure script in a package's source
    directory, and reads it's output to a string. From here, the
    string is broken up into a few different lists, made up of many
    strings. These lists are created by finding a unique header within
    the configure string, and then placing all of the important
    options into a single dictionary.

    This function returns a list containing sub-lists made up of the
    option flags, along with their brief help messages inside of
    strings. The output is generally sent directly to the
    option_processor function below.
    """

    configure_file_path = "%s/configure" % path
    output_string = subprocess.check_output([configure_file_path, '--help'])
    output_string = output_string.decode('utf-8')

    output_list = output_string.split('\n')

    option_start = find_first(output_list, "Optional Features:")
    option_end = find_first(output_list[option_start:], '') + option_start
    option_list = output_list[option_start + 1: option_end]

    install_start = find_first(output_list, "Fine tuning of the installation directories:")
    install_end = find_first(output_list[install_start:], '') + install_start
    install_dir_list = output_list[install_start + 1:install_end]

    return option_list, install_dir_list

def option_to_title(an_option):

    """ This function turns flags like '--disable-debug' into pretty
    titles, like 'Disable debug' for use in GUIs.
    """

    option = an_option.replace('-', ' ')
    option = option.lstrip(' ')
    option = option.title()

    return option

def option_processor(a_list):

    """ This function turns the list of sub-lists from
    get_config_lists, and turns them into a nicely formatted and
    ordered dictionary contain elements which will later be used by a
    GUI.

    This function returns a processed (Ordered) dictionary containing
    options in the format of:

        title: [raw_option_flag, help_message]
    """

    filtered_list = []
    output_dict = collections.OrderedDict()

    for item in a_list[1:]:
        line = autotool_filter(item)
        filtered_list.append(line)

    filtered_length = len(filtered_list)
    rev_range = list(reversed(range(filtered_length)))

    for index in rev_range:
        item = filtered_list[index]
        sub_items = len(item)

        if item[0] == '':
            for message_index in range(1, sub_items):
                clean_item = item[message_index].lstrip()
                filtered_list[index - 1].append(clean_item)

            filtered_list[index] = ''

        if sub_items > 2:
            item[1] = "%s %s" % (item[1], item[2])
            item.pop(2)

    for item in filtered_list:
        if isinstance(item, list):
            if 'FEATURE' in item[0]:
                continue

            title = option_to_title(item[0])
            opt_flag = item[0]
            help_message = item[1].capitalize()
            output_dict[title] = [opt_flag, help_message]
        else:
            filtered_list.remove(item)

    return output_dict

def install_flag_processor(a_list):

    """ Similar to the function above, this functions takes the
    option flags specific to directories where programs will be
    installed.

    This function returns an ordered dictionary containing install
    flags in the format of:

        raw_flag: [description, default_value]
    """
    install_flag_dict = collections.OrderedDict()

    for a_line in a_list:
        flag, message = (a_line.lstrip()).split(' ', 1)
        real_flag = flag[:-3]
        description, default_path = (message.lstrip()).rsplit(' ', 1)

        install_flag_dict[real_flag] = [description, default_path[1:-1]]

    return install_flag_dict
