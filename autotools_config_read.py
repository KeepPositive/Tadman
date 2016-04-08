#! /usr/bin/python3

## Standard
# N/A
## Dependencies
# N/A
## Scripts
# N/A

""" This script reads the output of autotools_config_write and turns them 
into a semi-usable list, which will later be processed further in 
autotools_config_proc.
"""

def find_first(search_list, length, phrase):
    
    """ This function looks for the first occurence of a string in a list. The
    search will only find a direct match to the string passed in as 'phrase'. 
    Note that if the list is made up of raw text taken from a terminal or 
    something of the sort, you may need to add a newline character (i.e. '\n')
    to the end of your 'phrase'. 

    This function returns the line number of the first occurence without any 
    padding (So the first line is 0, not 1).
    """
    
    for a_line in range(0, length):
        if search_list[a_line] == phrase:
            found_occurance = a_line
            break

    return found_occurance


def make_options_list(file_path):

    """ This function reads a file created by autotools_config_write and 
    filters it adds each one into a list. It then looks for a certain string 
    in the list (currently where the optional features begin) and saves the 
    line number to a variable. Afterwards, all items before this point are 
    deleted. Then it finds the next newline (AKA blank line) and saves that 
    to a variable and deletes everything following it. 
    
    This functions returns only the strings that contain optional features 
    which can be activated by the user. 
    """

    a_file = open(file_path, 'r')

    line_list = []
    file_lines = 0
    
    # Add all of lines from the file 'file_path' to the line 'line_list'
    for a_line in a_file:
        line_list.append(a_line)
        file_lines += 1
    
    a_file.close()

    start_line = find_first(line_list, file_lines, "Optional Features:\n")

    del line_list[0:start_line]

    lines_left = len(line_list)
    end_line = find_first(line_list, lines_left, "\n")

    del line_list[end_line:lines_left]

    return line_list
