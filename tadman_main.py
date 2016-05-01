#! /usr/bin/python3

## Standard
import os
import sys
## Dependencies
import click
## Scripts
import autotools_config_write
import autotools_config_read
import autotools_config_proc
import cmake_config_write
import cmake_config_read
import cmake_config_proc
import gtk_interface

@click.command()
@click.option('--dump', '-d', multiple=True, is_flag=True, 
              help="Print raw options list to stdout (for debugging)")
@click.option('--remove', '-r', multiple=True, is_flag=True, 
              help="Remove previous config_out.txt file")
@click.argument('path')
def main(path, remove, dump):

    configure_file_path = "%s/configure" % path
    cmakelists_file_path = "%s/CMakeLists.txt" % path
    config_out_file_path = "%s/config_out.txt" % path
    filtered_list = ()
    build_type = ()
   
    if remove:
        try:
            os.remove(config_out_file_path)
            print("Removed config_out.txt")
        except FileNotFoundError:
            print("Nothing to remove!")

    if os.path.isfile(configure_file_path):

        build_type = 'autotools'

        if os.path.isfile(config_out_file_path):
            print("Previous config_out.txt found!")
            config_options_list = autotools_config_read.make_options_list(config_out_file_path)
            filtered_list = autotools_config_proc.autotool_new_processor(config_options_list)
        else:
            autotools_config_write.write_config_txt(path)
            config_options_list = autotools_config_read.make_options_list(config_out_file_path)
            filtered_list = autotools_config_proc.autotool_new_processor(config_options_list)

    elif os.path.isfile(cmakelists_file_path):

        build_type = 'cmake'
        
        print("WARNING: CMake configuration requires dependencies installed prior to config.", 
              file=sys.stderr)

        if os.path.isfile(config_out_file_path):
            print("Previous config_out.txt found!")
            config_options_list = cmake_config_read.make_options_list(config_out_file_path)
            filtered_list = cmake_config_proc.cmake_processor(config_options_list)
        else:
            cmake_config_write.write_config_txt(path)
            config_options_list = cmake_config_read.make_options_list(config_out_file_path)
            filtered_list = cmake_config_proc.cmake_processor(config_options_list)
    
    else:
        print("This directory does not have a configure file.")
        sys.exit(97)

    if dump:
        print(config_options_list)

    interface = gtk_interface.gui_main(build_type, filtered_list)
    # Print the options once the GUI closes.
    print(interface)

if __name__ == '__main__':
    main()
