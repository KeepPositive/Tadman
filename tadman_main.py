#! /usr/bin/python3

## Standard
# N/A
## Dependencies
import click
## Scripts
import tadman_config_write
import tadman_config_read

@click.command()
@click.argument('path')
def main(path):

    config_txt_path = tadman_config_write.write_config_txt(path)
    config_options_list = tadman_config_read.make_options_list(config_txt_path)


    out_line_number = 0

    for a_line in config_options_list:
        print("%d\t%s" % (out_line_number, a_line), end="")
        out_line_number += 1

if __name__ == '__main__':
    main()
