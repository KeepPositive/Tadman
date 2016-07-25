""" Welcome to the Tadman ncurses interface. It's goal is to have all
the functionality of the GTK+ version, but use very few dependencies
and be accessible from a terminal interface.
"""
# Standard
import collections
import curses

def box_generator(title, box_y, box_x, displace_y, displace_x):

    """ This is a simple function which returns a curses-based box
    object, in order to remove some clutter later on. It even adds
    a cute title to the top of each box :D
    """

    new_box = curses.newwin(box_y, box_x, displace_y, displace_x)
    new_box.box()
    new_box.addstr(0, 1, " %s " % title.upper())

    return new_box

def line_wrapper(a_string, length):

    """ This function is responsible for 'wrapping' long strings. This
    is achieved by setting a desire length, and then finding the space
    character nearest to said length. Strings of the desire length are
    then added to a dictionary.

    The return value of this function is a list containing multiple
    strings.
    """

    string_list = [a_string]
    count = 0

    while count < len(string_list):
        for string in string_list:

            str_length = len(string)

            if str_length > length and ' ' in string[:length]:
                for index in reversed(range(length)):
                    if string[index] == ' ':
                        str_split = string[:index]
                        str_remainder = string[index + 1:]

                        string_list.remove(string)
                        string_list.append(str_split)
                        string_list.append(str_remainder)
                        count += 1
                        break
            else:
                count += 1

        return string_list

class CursesInterface():

    """ This is the class for the Tadman curses interface. It is
    relatively simple, but still retains a large amount of
    functionality.
    """

    def __init__(self, a_dict, name, version, build_system):

        self.option_dict = a_dict
        self.option_list = []
        self.toggle_dict = {}

        for item in self.option_dict:
            self.option_list.append(item)
            self.toggle_dict[item] = False

        self.package_name = name
        self.package_version = version
        self.build_type = build_system

        # Initialize the main screen
        self.screen = curses.initscr()
        curses.echo()
        curses.cbreak()
        self.screen.keypad(1)
        # Add a title to the main screen
        self.screen.addstr(0, 1, "Tadman Package Manager", curses.A_UNDERLINE)
        # Add a small help message that will be covered up later
        self.screen.addstr(12, 41, "NOTE: If no value is entered,")
        self.screen.addstr(13, 41, "the default will be selected")

        # Create a sub window for the options list
        self.option_box = box_generator('options', 20, 36, 2, 0)
        self.option_box.scrollok(True)

        # Create a sub window for package information
        self.pack_info_box = box_generator('package info', 9, 44, 2, 36)
        # Add some title lines
        self.pack_info_box.addstr(2, 2, "Package:", curses.A_BOLD)
        self.pack_info_box.addstr(3, 2, "Version:", curses.A_BOLD)
        self.pack_info_box.addstr(4, 2, 'DestDir:', curses.A_BOLD)
        self.pack_info_box.addstr(5, 2, 'FldName:', curses.A_BOLD)
        self.pack_info_box.addstr(6, 2, 'BldType:', curses.A_BOLD)
        # Display available values along with titles
        self.pack_info_box.addstr(4, 11, '/usr/local/tadman')
        self.pack_info_box.addstr(6, 11, self.build_type)

        # Create a sub window for option information
        self.opt_info_box = box_generator('option info', 11, 44, 11, 36)
        self.opt_info_box.addstr(2, 2, "# of options: ", curses.A_BOLD)
        self.opt_info_box.addstr(2, 16, str(len(self.option_dict)))
        self.opt_info_box.addstr(3, 2, "Option index:", curses.A_BOLD)
        self.opt_info_box.addstr(4, 2, "Flag:", curses.A_BOLD)
        self.opt_info_box.addstr(5, 2, "Help Message:", curses.A_BOLD)
        # Print a little help message
        self.screen.addstr(22, 10, "Hit 'enter' to select items, 'q' to quit or 'e' to execute")

    def refresh_options(self):

        """ This quaint little function reads the option dictionary,
        and prints out checkboxes according to whether the value is
        True or False.
        """

        offset_y = 2
        # For each item, print an X or not depending on the current state
        for item in self.option_list[:16]:
            if self.toggle_dict[item]:
                self.option_box.addstr(offset_y, 2, "[X] %s" % item)
            else:
                self.option_box.addstr(offset_y, 2, "[ ] %s" % item)
            offset_y += 1

    def refresh_option_info_box(self, index):

        """ While moving the cursor up and down within the interface,
        the option info box must be updated with information pertinent
        to the highlighted item. In order to keep these all in track
        and make the main_loop function slightly cleaner, this function
        updates the information by itself. Prior to writing, it also
        overwrites old info with whitespace.
        """

        current_item = self.option_list[index]

        message_height = 6
        # Overwrite old info with spaces
        self.opt_info_box.addstr(3, 16, '  ')
        self.opt_info_box.addstr(4, 8, ' ' * 35)

        for line_y in [6, 7, 8]:
            self.opt_info_box.addstr(line_y, 2, ' ' * 36)
        # Gather and print out new information
        option_flag, original_help_message = self.option_dict[current_item]
        #option_flag = ''
        #original_help_message = self.option_dict[current_item]
        wrapped_help_message = line_wrapper(original_help_message, 36)

        self.opt_info_box.addstr(3, 16, "%i" % index)
        self.opt_info_box.addstr(4, 8, option_flag)

        for a_line in wrapped_help_message:
            self.opt_info_box.addstr(message_height, 2, str(a_line))
            message_height += 1

    def refresh_main_screen(self):

        """ This function is pretty self-explanitory. It simply
        refreshes all of the main windows.
        """

        self.screen.refresh()
        self.refresh_options()
        self.option_box.refresh()
        self.pack_info_box.refresh()
        self.opt_info_box.refresh()

    def get_return_values(self):

        return_list = []

        for string in [self.package_name, self.package_version]:
            if isinstance(string, bytes):
                return_list.append(string.decode('utf-8'))
            else:
                return_list.append(string)

        index_list = []

        for item in self.toggle_dict:
            if self.toggle_dict[item]:
                index_list.append(self.option_list.index(item))

        return_list.append(sorted(index_list, key=int))
        # Return a version of the list that is sorted by value
        return return_list

    def main_loop(self):

        """ This is the main loop of the interface. It deals with
        a large majority of the user input.
        """

        self.screen.refresh()
        pack_name = self.pack_info_box.getstr(2, 11, 27)[:26]
        pack_version = self.pack_info_box.getstr(3, 11, 27)[:26]
        # Disable the users ability to type freely
        curses.noecho()
        # If the line is left empty, display the default value
        if pack_name.decode('utf-8') != '':
            self.package_name = pack_name.decode('utf-8')

        if pack_version.decode('utf-8') != '':
            self.package_version = pack_version.decode('utf-8')

        self.pack_info_box.addstr(2, 11, self.package_name)
        self.pack_info_box.addstr(3, 11, self.package_version)

        output_folder = "%s-%s" % (self.package_name, self.package_version)
        self.pack_info_box.addstr(5, 11, output_folder)
        # Add some more lines to the package info box
        self.refresh_option_info_box(0)

        self.refresh_main_screen()
        # Move the cursor to the start of the options list
        self.screen.move(4, 3)

        key = ''
        exit_interface = True
        # Read incoming keypresses until quit or execute
        while exit_interface:

            key = self.screen.getch()
            current_y, current_x = self.screen.getyx()
            current_index = current_y - 4
            # When 'q'  or 'e' is pressed, close window
            if key == ord('q') or key == ord('e'):
                exit_interface = False
            # When the up arrow is pressed, reduce y-value to move cursor up
            elif key == curses.KEY_UP:
                if current_y > 4:
                    current_y -= 1
                    current_index -= 1
            #  When the down arrow is pressed, increase y-value to move cursor
            # down
            elif key == curses.KEY_DOWN:
                if current_y < 3 + len(self.option_list) and current_y < 19:
                    current_y += 1
                    current_index += 1
            #  If 'enter' is pressed, add an X to the option by altering a
            # dictionary and refreshing the interface
            elif key == ord('\n'):
                current_item = self.option_list[current_index]
                new_value = not self.toggle_dict[current_item]
                self.toggle_dict[current_item] = new_value

                self.refresh_options()
                self.option_box.refresh()

            self.refresh_option_info_box(current_index)
            self.opt_info_box.refresh()

            self.screen.move(current_y, current_x)
            self.screen.refresh()

        curses.endwin()
        # Following a quit or execute, do some things
        if key == ord('q'):
            print("Tadman build canceled")
            return False
        elif key == ord('e'):
            return True


if __name__ == '__main__':
    IN_LIST = [('Enable verbose build', ['--enable-verbose',
                                         'Output extra info while configuring']),
               ('Enable unicode support', ['--enable-unicode',
                                           'UTF-8 is the true master race!']),
               ('Disable squid mode', ['--disable-squid', 'What does this do?']),
               ('Disable colored output', ['--disable-color',
                                           'Disable color for those that are colorblind']),
               ('Use old legacy driver', ['--enable-legacy-driver',
                                          'For lovers of classic Linux 2.4'])]
    ORD_DICT = collections.OrderedDict(IN_LIST)
    N_INTERFACE = CursesInterface(ORD_DICT, 'squid', '1.4.18', 'autotools')
    if N_INTERFACE.main_loop():
        print(N_INTERFACE.get_option_values())
        print(N_INTERFACE.get_entry_values())
