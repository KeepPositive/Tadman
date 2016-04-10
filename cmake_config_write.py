#! /usr/bin/python3

## Standard
import os
import shutil
import subprocess
## Dependencies
# N/A
## Scripts
# N/A

""" This script creates a config_out.txt for source code using the CMake build
system.
"""

def write_config_txt(path):

    """ This function runs the CMake command (which unlike Autotools, CMake runs
    the configure process before it can print the help options) and then sends
    the useful options into the 'config_out.txt' file. In order to do this, a 
    build directory (called 'tadman_build'). If this folder already exists, it
    is emptied first.
    """

    cmakelist_file_path = "%s/CMakeLists.txt" % path
    config_out_path = "%s/config_out.txt" % path
    cmake_build_dir = "%s/tadman_build" % path
    
    # If the tadman_build directory exists, remove it.
    if os.path.isdir(cmake_build_dir):
        shutil.rmtree(cmake_build_dir)
    
    # Create or recreate the tadman_build dir.
    os.makedirs(cmake_build_dir)
    # Change to the directory so files will be stored there.
    os.chdir(cmake_build_dir)

    a_file = open(config_out_path, 'w')

    subprocess.run(['cmake', path, '-LH'], stdout=a_file)

    a_file.close()
