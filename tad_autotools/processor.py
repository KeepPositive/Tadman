
""" This script is responsible with turning the filtered list output by
autotools_config_read into a squeaky clean list of lists of strings which
which can be utilized by one of the GUIs.
"""

## Standard
import collections

def autotool_filter(a_string):

    """ This function simply removes the '--' before each option and the
    newline character ('\n') from each string, and then splits the option
    from the message at the first space it sees.

    This function returns a pair consisting of a raw option, and a raw
    message which will be cleaned up later.
    """

    filtered_pair = a_string[2:-1].split(' ', 1)

    if len(filtered_pair) > 1:
        filtered_pair[1] = filtered_pair[1].lstrip()

    return filtered_pair


def blank_removal(a_list):

    """ This one is a little complicated. It is used in the processor function
    to clean up areas where the help option explain message runs onto a new
    line. All messages are eventually thrown into one long string.
    """

    new_list = []

    for part in a_list:
        if part == '':
            pass
        else:
            new_list.append(part.lstrip(' '))

    return new_list


def autotool_clean(a_pair):

    """ This is where the real cleaning occurs. It takes in a pair, consisting
    of an option, and a message. The help options (first in the pair) are made
    into spiffy title-like strings. The first letters of the messages are
    capitalized. It also removes all preceeding spaces from both strings.

    This function returns a list consisting of three items: the cleaned
    'option title', the original option in its raw form, and the cleaned up
    message.
    """

    clean_first = a_pair[0].replace('-', ' ')
    clean_first = clean_first.lstrip(' ')
    clean_first = clean_first.title()
    clean_second = a_pair[1].lstrip()
    clean_second = clean_second.capitalize()

    return [clean_first, a_pair[0], clean_second]


def autotool_message_merge(a_pair):

    """ A pair is only supposed to consist of two items. If there are more
    than two, then the the ones at the end are combined, until there are only
    two items in the pair.

    WARNING: This function isn't even used, but it might be helpful later. I
    don't really know.
    """

    lines_of_message = len(a_pair)
    base_message = a_pair[1]

    for x in range(1, lines_of_message):
        print(a_pair(x))

def option_to_title(an_option):

    option = an_option.replace('-', ' ')
    option = option.lstrip(' ')
    option = option.title()

    return option

def autotool_newer_processor(a_list):

    """ This is kinda like the main function of the script. It essentially
    uses all the functions above in a kinda smart way to clean up all of
    the lines from autotools_config_write.

    This function returns a processed dictionary containing options in the
    format of:

        title: [cli_option, help_message]
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
            for x in range(1, sub_items):
                clean_item = item[x].lstrip()
                filtered_list[index - 1].append(clean_item)

            filtered_list[index] = ''

        if sub_items > 2:
            item[1] = "%s %s" % (item[1], item[2])
            item.pop(2)

    for item in filtered_list:
        if isinstance(item, list):
            title = option_to_title(item[0])
            opt_flag = item[0]
            help_message = item[1].capitalize()
            output_dict[title] = [opt_flag, help_message]
        else:
            filtered_list.remove(item)

    return output_dict
