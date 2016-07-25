import tad_autotools.processor as aproc
import tad_autotools.reader as aread
import tad_autotools.writer as awrite
import tad_interface.curses_main
import tad_interface.gtk_main
import tad_tools.config_build

def tester(a_path):
    config_out_file_path = "%s/config_out.txt" % a_path

    awrite.write_config_txt(a_path)
    raw_options_list = aread.make_options_list(config_out_file_path)
    filtered_options_dict = aproc.autotool_newer_processor(raw_options_list)

    return filtered_options_dict

if __name__ == '__main__':
    test_dict = tester("/home/tedm1/Source/openbox-3.6.1")
    #print(test_dict)
    """
    option_list = []
    for item in test_dict:
        option_list.append(item)

    print(option_list)
    for item in option_list:
        print(test_dict[item][1])
    """
    #"""
    interface = tad_interface.curses_main.CursesInterface(test_dict, 'openbox',
                                                          '3.6.1', 'autotools')
    if interface.main_loop():
        inter_out = interface.get_return_values()
        #print(inter_out)
    #"""
    """
    interface = tad_interface.gtk_main.gui_main(test_dict, 'openbox',
                                                '3.6.1', 'autotools')
    print(interface)
    """
    #"""
    conf = tad_tools.config_build.configure_maker(test_dict, inter_out[2], 'autotools')
    #print(conf)
    #"""
