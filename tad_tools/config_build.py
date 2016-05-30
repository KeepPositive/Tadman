#! /usr/bin/python3

import os
import subprocess

configure_list = []

def configure_maker(mode, in_list):

    configure_list = []

    if mode == 'autotools':
        configure_list.append('./configure')
        configure_list.append('--prefix=/usr')
    
    elif mode == 'cmake':
        configure_list.append('cmake')
        configure_list.append('-DCMAKE_INSTALL_PREFIX=/usr')

    #print(in_list)

    for x in in_list[2]:
        configure_list.append(x)

    return configure_list
