#! /usr/bin/python3

import os
import subprocess

def configure_maker(in_dict, in_list, mode):

    configure_indexes = in_list
    configure_list = []
    option_list = []

    for item in in_dict:
        configure_list.append(item)

    if mode == 'autotools':
        option_list.append('./configure')
        option_list.append('--prefix=/usr')

    elif mode == 'cmake':
        option_list.append('cmake')
        option_list.append('-DCMAKE_INSTALL_PREFIX=/usr')

    for index in configure_indexes:
        option = in_dict[configure_list[index]][0]

        if mode == 'cmake':
            option = "%s%s" % (option, 'ON')

        option_list.append(option)

    return option_list
