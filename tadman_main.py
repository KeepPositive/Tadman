#! /usr/bin/python3

## Standard
import sys
## Dependencies
import click
## Scripts
import autotools_config_write
import autotools_config_read
import autotools_config_proc

@click.command()
@click.argument('path')
def main(path):

    config_txt_path = autotools_config_write.write_config_txt(path)
    
    if config_txt_path == None:
        print("This directory does not have a configure file.")
        sys.exit(97)
    config_options_list = autotools_config_read.make_options_list(config_txt_path)
    filt_list = autotools_config_proc.autotool_new_processor(config_options_list)

    for x in filt_list:
        print(x)


if __name__ == '__main__':
    main()
