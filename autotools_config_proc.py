#! /usr/bin/python3

## Standard
# N/A
## Dependencies
# N/A
## Scripts
# N/A

def autotool_filter(a_string):
    
    filtered_pair = a_string[2:-1].split(' ', 1)

    return filtered_pair 


def blank_removal(a_list):
    
    new_list = []

    for part in a_list:
        if part == '':
            pass
        else:
            new_list.append(part.lstrip(' '))

    return new_list

        
def autotool_clean(a_pair):
    
    clean_first = a_pair[0].replace('-', ' ')
    clean_first = clean_first.lstrip(' ')
    clean_first = clean_first.title()
    clean_second = a_pair[1].lstrip()
    clean_second = clean_second.capitalize()

    return([clean_first, a_pair[0], clean_second])


def autotool_message_merge(a_pair):
    
    lines_of_message = len(a_pair)
    base_message = a_pair[1]
    
    for x in range(1, lines_of_message):
        print(a_pair(x))


def autotool_new_processor(a_list):

    filtered_list = []
    processed_list = []

    for a_string in a_list [1:]:
        filtered_list.append(autotool_filter(a_string))

    index_offset = 0
    count = 1
    
    while count < 3:
        for x in filtered_list:
            
            index = filtered_list.index(x) - index_offset
            pair_length = len(x)

            if x[0] == '':
                filtered_list[index - (1 + index_offset)].append(x[1])
                filtered_list.pop(index - (index_offset))
        count += 1
    
    for y in filtered_list:
        
        index = filtered_list.index(y)

        if len(y) > 2:

            new_message = "%s %s" % (y[1], y[2].lstrip())
            new_pair = [y[0], new_message]
            filtered_list.remove(y)
            filtered_list.insert(index, new_pair)

    for z in filtered_list:
        processed_list.append(autotool_clean(z))

    return processed_list
