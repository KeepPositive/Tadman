#! /usr/bin/python3

## Standard
# N/A
## Dependencies
# N/A
## Scripts
# N/A

def find_first(search_list, length, phrase):
    for a_line in range(0, length):
        if search_list[a_line] == phrase:
            found_occurance = a_line
            break

    return found_occurance


def make_options_list(file_path):

    a_file = open(file_path, 'r')

    line_list = []
    file_lines = 0

    for a_line in a_file:
        line_list.append(a_line)
        file_lines += 1

    start_line = find_first(line_list, file_lines, "Optional Features:\n")

    del line_list[0:start_line]

    lines_left = len(line_list)
    end_line = find_first(line_list, lines_left, "\n")

    del line_list[end_line:lines_left]

    return line_list
