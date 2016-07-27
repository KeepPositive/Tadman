""" This script contains several functions that deal with the careful
handling of paths.
"""

# Standard
import os

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

def last_slash_check(a_path):

    """Check if the path provided has an ending slash. If it does, remove
    it and return a revised path. If not, do nothing.
    """

    if a_path[-1] == '/':
        new_path = a_path[:-1]
    else:
        new_path = a_path

    return new_path

def path_spliter(a_path):

    """ Since os.path.basename is not completely reliable when finding the
    basename of a directory (the user may enter it ending with a slash) so
    this script finds the true last directory.

    This function returns the name of the last branch in a directory path.
    """

    path_split = a_path.split(sep='/')

    if a_path[-1] == '/':
        directory_name = path_split[-2]
    else:
        directory_name = path_split[-1]

    return directory_name


def last_character_split(a_name, char):

    """ In order to split the name and version of a package in a
    standardly named source code directory, one must split the two at a
    standard spot. Some packagers use a '-', like in the file name
    'openbox-3.6.1'. This function splits a name by whatever character it
    is given as its second argument.

    This function returns a tuple of the title and version. If it does not
    detect a version number, then the whole name is likely a title, and the
    version is returned as an empty string.
    """

    dash_index = a_name.rfind(char)

    if a_name[dash_index + 1].isdigit():
        title, version = a_name.rsplit(char, 1)
    else:
        title = a_name.replace(char, '-')
        version = "N/A"

    return title, version


def digit_split(a_name):

    """ This function deals with digits inside of a string. """
    name_length = len(a_name)
    index = 0
    digit_count = 0
    split_or_not = False
    split_index = 0

    print(name_length - 1)
    while (index < (name_length - 1)) and (digit_count < 2):
        if a_name[index].isdigit():
            digit_count += 1

            if digit_count == 1:
                split_index = index
            elif digit_count == 2:
                split_or_not = True
                break

        print(index)
        index += 1

    if split_or_not:
        name = a_name[:split_index]
        version = a_name[split_index:]
    else:
        name = a_name
        version = ""

    return name, version


def name_version_split(a_path):

    """ As the title states, this function reads a folder title, and
    splits the package name and version (if available) from it. It
    specializes in reading packages which are named 'name-version',
    but it can read a few others.
    """

    digit_in_name = False

    a_name = path_spliter(a_path)

    for char in a_name:
        if char.isdigit():
            digit_in_name = True

    if digit_in_name:
        if '-' in a_name:
            split = last_character_split(a_name, '-')
        elif '_' in a_name:
            split = last_character_split(a_name, '_')
        else:
            split = digit_split(a_name)

    else:
        split = (a_name, '')

    return split
