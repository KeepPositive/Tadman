""" Welcome to the Tadman ncurses interface. It's goal is to have all
the functionality of the GTK+ version, but use very few dependencies
and be accessible from a terminal interface.
"""

# Standard
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

class MainInterface():

    """ This is the class for the Tadman curses interface. It is
    relatively simple, but still retains a large amount of
    functionality.
    """

    def __init__(self, a_dict):

        self.option_dict = a_dict
        self.package_name = ''
        self.package_version = ''
        self.build_type = ''

        self.option_list = []
        self.toggle_dict = {}
        self.options_avail = 0

        for item in self.option_dict:
            self.option_list.append(item)
            self.toggle_dict[item] = False
            self.options_avail += 1


        # Initialize and prepare the main screen
        self.screen = curses.initscr()
        curses.echo()
        curses.cbreak()
        self.screen.keypad(1)
        # Add a title to the main screen
        self.screen.addstr(0, 1, "Tadman Package Manager", curses.A_UNDERLINE)
        # Print a little help message
        self.screen.addstr(22, 10,
                           "Hit 'enter' to select items, 'q' to quit or 'e' to execute")
        # Add a small help message that will be covered up later
        self.screen.addstr(12, 41, "NOTE: If no value is entered,")
        self.screen.addstr(13, 41, "the default will be selected")

        # Start initializing subwindows
        # Create a sub window that will contain the options list
        self.option_box = box_generator('options', 20, 36, 2, 0)
        # Create a pad window for the actual options list
        self.option_pad = curses.newpad(self.options_avail + 4, 36)

        # Create a sub window for package information
        self.pack_info_box = box_generator('package info', 9, 44, 2, 36)

        # Create a sub window for option information
        self.opt_info_box = box_generator('option info', 11, 44, 11, 36)


    def init_package_info_entry(self):

        """ Once the script begins, it is a good idea to run this
        function. It allows the user to enter vital package info
        easily and efficiently.
        """

        # Add some title lines
        self.pack_info_box.addstr(2, 2, "Package:", curses.A_BOLD)
        self.pack_info_box.addstr(3, 2, "Version:", curses.A_BOLD)
        self.pack_info_box.addstr(4, 2, 'DestDir:', curses.A_BOLD)
        self.pack_info_box.addstr(5, 2, 'FldName:', curses.A_BOLD)
        self.pack_info_box.addstr(6, 2, 'BldType:', curses.A_BOLD)

        # Now we begin the program
        self.screen.refresh()
        # Get some user input
        pack_name = self.pack_info_box.getstr(2, 11, 27).decode('utf-8')
        pack_version = self.pack_info_box.getstr(3, 11, 27).decode('utf-8')
        # Disable the users ability to type freely
        curses.noecho()
        # If the line is left empty, display the default value
        if pack_name:
            self.package_name = pack_name[:26]

        if pack_version:
            self.package_version = pack_version[:26]

        output_folder = "%s-%s" % (self.package_name, self.package_version)
        # Display information next to the titles
        self.pack_info_box.addstr(2, 11, self.package_name)
        self.pack_info_box.addstr(3, 11, self.package_version)
        self.pack_info_box.addstr(4, 11, '/usr/local/tadman')
        self.pack_info_box.addstr(5, 11, output_folder)
        self.pack_info_box.addstr(6, 11, self.build_type)
        self.pack_info_box.refresh()

    def refresh_options_list(self):

        """ This quaint little function reads the option dictionary,
        and prints out checkboxes according to whether the value is
        True or False.
        """

        offset_y = 0
        # For each item, print an X or not depending on the current state
        for item in self.option_list:
            if self.toggle_dict[item]:
                self.option_pad.addstr(offset_y, 0, "[X] %s" % item)
            else:
                self.option_pad.addstr(offset_y, 0, "[ ] %s" % item)
            offset_y += 1

        self.option_box.refresh()

    def refresh_option_info_box(self, index):

        """ While moving the cursor up and down within the interface,
        the option info box must be updated with information pertinent
        to the highlighted item. In order to keep these all in track
        and make the main_loop function slightly cleaner, this function
        updates the information by itself. Prior to writing, it also
        overwrites old info with whitespace.
        """

        current_item = self.option_list[index]

        # Overwrite old info with spaces
        self.opt_info_box.addstr(2, 16, ' ' * 5)
        self.opt_info_box.addstr(3, 8, ' ' * 35)

        for line_y in [5, 6, 7, 8]:
            self.opt_info_box.addstr(line_y, 2, ' ' * 40)

        # Gather and print out new information
        option_flag, original_help_message = self.option_dict[current_item]
        wrapped_help_message = line_wrapper(original_help_message, 40)

        pretty_index = str(index + 1).zfill(2)
        self.opt_info_box.addstr(2, 16,
                                 "%s/%i" % (pretty_index, self.options_avail))
        self.opt_info_box.addstr(3, 8, option_flag)

        message_height = 5
        for a_line in wrapped_help_message:
            self.opt_info_box.addstr(message_height, 2, str(a_line))
            message_height += 1

        self.opt_info_box.refresh()

    def refresh_option_windows(self):

        """ This method is pretty self-explanitory. It simply
        refreshes all of the main windows that have to do with
        choosing options.
        """

        self.screen.refresh()
        self.refresh_options_list()
        self.option_box.refresh()
        self.opt_info_box.refresh()

    def get_return_values(self):

        """ This function simple returns all of the useful user input
        that was gathered by the interface.

        This input is returned in a list as follows:

        [package_name, package_version, [indexes of options chosen]]
        """

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

    def init_option_loop(self):

        """ This method prepares the option choosing windows with
        titles and other indicators to benefit the user experience.
        Finally, it refreshes all of the necessary windows.
        """

        # Set up the option info box for feature options
        self.opt_info_box.addstr(2, 2, "Option index:", curses.A_BOLD)
        self.opt_info_box.addstr(3, 2, "Flag:", curses.A_BOLD)
        self.opt_info_box.addstr(4, 2, "Help Message:", curses.A_BOLD)
        # If there are more options than available, indicate it
        if self.options_avail > 15:
            self.option_box.addstr(18, 13, "▼ More ▼", curses.A_BOLD)

        # Initialize the info in the option info box
        self.refresh_option_info_box(0)
        self.refresh_option_windows()
        self.option_pad.refresh(0, 0, 4, 2, 19, 34)
        # Move the cursor to the start of the options list
        self.screen.move(4, 3)

    def run_option_loop(self):

        """ This is the option loop. It is in charge of controlling
        the cursors position and the selection of items within the
        option interface.
        """

        key = ''
        exit_interface = True

        pad_offset = 0
        window_offset = 4
        index_offset = window_offset + pad_offset
        maximum_offset = self.options_avail - 16
        maximum_y = self.options_avail + 3
        # Read incoming keypresses until quit or execute
        while exit_interface:

            key = self.screen.getch()
            current_y, current_x = self.screen.getyx()
            current_index = current_y - index_offset

            # When 'q'  or 'e' is pressed, close window
            if key in [ord('e'), ord('q')]:
                exit_interface = False

            # When the up arrow is pressed, reduce y-value or scroll list up
            if key == curses.KEY_UP:
                if current_y == 4 and pad_offset > 0:
                    pad_offset -= 1
                elif current_y > 4:
                    current_y -= 1

            #  When the down arrow is pressed, increase y or scroll list down
            elif key == curses.KEY_DOWN:
                if current_y == 19 and pad_offset < maximum_offset:
                    pad_offset += 1
                elif current_y < 19 and current_y < maximum_y:
                    current_y += 1
            # When 'HOME' is pressed, scroll to top of list
            elif key == curses.KEY_HOME:
                current_y = 4
                pad_offset = 0
            # When 'END' is pressed, scroll to bottom of list
            elif key == curses.KEY_END:
                if self.options_avail > 15:
                    current_y = 19
                    pad_offset = maximum_offset
                else:
                    current_y = self.options_avail + 3


            current_index = current_y + pad_offset - window_offset

            #  If 'enter' is pressed, add an X to the option by altering a
            # dictionary and refreshing the interface
            if key == ord('\n'):
                current_item = self.option_list[current_index]
                new_value = not self.toggle_dict[current_item]
                self.toggle_dict[current_item] = new_value

                self.refresh_options_list()

            self.option_pad.refresh(pad_offset, 0, 4, 2, 19, 34)

            # Special chars: ▲ ▼ ↑ ↓
            # While scrolling, indicate where there are more options available
            if pad_offset > 0:
                self.option_box.addstr(1, 13, "▲ More ▲", curses.A_BOLD)
            else:
                self.option_box.addstr(1, 13, ' ' * 8)

            if pad_offset < maximum_offset:
                self.option_box.addstr(18, 13, "▼ More ▼", curses.A_BOLD)
            else:
                self.option_box.addstr(18, 13, ' ' * 8)

            self.option_box.refresh()
            self.refresh_option_info_box(current_index)

            self.screen.move(current_y, current_x)
            self.screen.refresh()

        curses.endwin()

        # Return a value based on how the window was closed
        if key == ord('q'):
            return False
        elif key == ord('e'):
            return True


def main_loop(a_dict, name, version, build_type):

    """ This is a simple function with the goal of making scripts that
    utilize this interface more clean. It sets all of the vital info,
    and runs all of the major loops available in a specific order.
    """

    interface = MainInterface(a_dict)

    interface.package_name = name
    interface.package_version = version
    interface.build_type = build_type

    interface.init_package_info_entry()

    interface.init_option_loop()
    interface.run_option_loop()

    return interface.get_return_values()
