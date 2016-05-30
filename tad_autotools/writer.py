#! /usr/bin/python3

## Standard
import subprocess
## Dependencies
# N/A
## Scripts
# N/A

""" This script reads an Autotools help message and outputs the message to a 
file.
"""

def write_config_txt(path):

    """ As stated above, this function reads the help message from the basic
    autotools configure file, and outputs the message to a file called 
    'config_out.txt'. 
    
    This function returns nothing.
    """

    configure_file_path = "%s/configure" % path
    config_out_path = "%s/config_out.txt" % path
        
    a_file = open(config_out_path, 'w')

    subprocess.run([configure_file_path, '--help'], stdout=a_file)

    a_file.close()
