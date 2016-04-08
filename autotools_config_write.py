#! /usr/bin/python3

## Standard
import os
import subprocess
## Dependencies
# N/A
## Scripts
# N/A

""" This function reads the help message from the configure file, and outputs
the message to a file.
"""

def write_config_txt(path):

    """ As stated above, this function reads the help message from the
    configure file, and outputs the message to a file called 'config_out.txt'. 
    
    This function returns the path to the 'config_out.txt'. If the file path 
    that it is given does not exist, it returns a None.
    """

    in_path = path
    configure_file_path = "%s/configure" % in_path
    
    if os.path.isfile(configure_file_path):
    
        config_out_path = "%s/config_out.txt" % in_path
        
        a_file = open(config_out_path, 'w')

        subprocess.run([configure_file_path, '--help'], stdout=a_file)

        a_file.close()
    
    else:
        config_out_path = None

    return config_out_path
