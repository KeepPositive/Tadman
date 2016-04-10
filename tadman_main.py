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

@click.command()
@click.option('--remove', '-r', multiple=True, is_flag=True, 
              help="Remove previous config_out.txt file.")
@click.argument('path')
def main(path, remove):

    configure_file_path = "%s/configure" % path
    cmakelists_file_path = "%s/CMakeLists.txt" % path
    config_out_file_path = "%s/config_out.txt" % path
   
    if remove:
        try:
            os.remove(config_out_file_path)
            print("Removed config_out.txt")
        except FileNotFoundError:
            print("Nothing to remove!")

    if os.path.isfile(configure_file_path):

        if os.path.isfile(config_out_file_path):
            print("Previous config_out.txt found!")
            config_options_list = autotools_config_read.make_options_list(config_out_file_path)
            filt_list = autotools_config_proc.autotool_new_processor(config_options_list)
        else:
            autotools_config_write.write_config_txt(path)
            config_options_list = autotools_config_read.make_options_list(config_out_file_path)
            filt_list = autotools_config_proc.autotool_new_processor(config_options_list)

        for x in filt_list:
            print(x)

    elif os.path.isfile(cmakelists_file_path):
        print("Found CMake file.")
        print("WARNING: CMake configuration requires dependencies installed prior to config.")

        if os.path.isfile(config_out_file_path):
            print("Previous config_out.txt found!")
            config_options_list = cmake_config_read.make_options_list(config_out_file_path)
            filtered_list = cmake_config_proc.cmake_processor(config_options_list)
        else:
            cmake_config_write.write_config_txt(path)
            config_options_list = cmake_config_read.make_options_list(config_out_file_path)
            filtered_list = cmake_config_proc.cmake_processor(config_options_list)

        for y in filtered_list:
            print(y)

    else:
        print("This directory does not have a configure file.")
        sys.exit(97)

if __name__ == '__main__':
    main()
