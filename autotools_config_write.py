#! /usr/bin/python3

## Standard
import os
import subprocess
## Dependencies
# N/A
## Scripts
# N/A

def write_config_txt(path):

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
