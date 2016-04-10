#! /usr/bin/python3

## Standard
## Dependencies
## Scripts

""" This script reads the config_out.txt and turns it into a list of the 
useful options the user can change.
"""

def make_options_list(file_path):

    """ This function reads the config_out.txt created by cmake_config_write
    and turns it into a list which can be read by cmake_config_proc. It uses
    two lists: one for the lines directly from the file, and the other made up
    of useful options for the user to switch on or off.

    This function returns a list of lists containing a help message and an 
    option, respectively.
    """

    a_file = open(file_path, 'r')

    line_list = []
    option_list = []
    file_lines = 0

    for a_line in a_file:
        line_list.append(a_line)
        file_lines += 1
    # Items with 'BOOL' are on or off switches which can be changed.
    for index in range(file_lines - 1):
        if 'BOOL' in line_list[index]:
            option_list.append([line_list[index - 1], line_list[index]]) 
    
    return option_list 
