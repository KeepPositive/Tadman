import tad_autotools.processor as aproc
import tad_autotools.reader as aread
import tad_autotools.writer as awrite

def tester(a_path):
    config_out_file_path = "%s/config_out.txt" % a_path

    awrite.write_config_txt(a_path)
    raw_options_list = aread.make_options_list(config_out_file_path)
    filtered_options_list = aproc.autotool_newer_processor(raw_options_list)

    for x in filtered_options_list:
        print("%s: %s" % (x, filtered_options_list[x][0]))
        print("  %s" % filtered_options_list[x][1])
if __name__ == '__main__':
    tester("/home/tedm1/Source/openbox-3.6.1")
