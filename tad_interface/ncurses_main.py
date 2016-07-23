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

class CursesInterface():

    """ This is the class for the Tadman curses interface. It is
    relatively simple, but still retains a large amount of
    functionality.
    """

    def __init__(self, opt_list, name, version, build_system):

        self.option_list = opt_list
        self.option_dict = {}

        for item in self.option_list:
            self.option_dict[item] = False

        self.package_name = name
        self.package_version = version
        self.build_type = build_system

        # Initialize the main screen
        self.screen = curses.initscr()
        curses.echo()
        curses.cbreak()
        self.screen.keypad(1)
        self.screen.addstr(0, 1, "Tadman Package Manager", curses.A_UNDERLINE)
        self.screen.refresh()
        # Create a sub window for the options list
        self.option_box = box_generator('options', 20, 36, 2, 1)
        # Create a sub window for package information
        self.pack_info_box = box_generator('package info', 10, 36, 2, 37)
        self.pack_info_box.addstr(2, 2, "Package:", curses.A_BOLD)
        self.pack_info_box.addstr(3, 2, "Version:", curses.A_BOLD)
        # Create a sub window for option information
        self.opt_info_box = box_generator('option info', 10, 36, 12, 37)
        self.opt_info_box.addstr(2, 2, "# of options: %i" % len(self.option_list))
        # Print a little help message
        self.screen.addstr(22, 18, "Hit 'q' to quit or 'e' to execute")

    def refresh_options(self):

        """ This quaint little function reads the option dictionary,
        and prints out checkboxes according to whether the value is
        True or False.
        """

        offset_y = 2
        # For each item, print an X or not depending on the current state
        for item in self.option_list:
            if self.option_dict[item]:
                self.option_box.addstr(offset_y, 2, "[X] %s" % item)
            else:
                self.option_box.addstr(offset_y, 2, "[ ] %s" % item)
            offset_y += 1

    def refresh_main_screen(self):

        """ This function is pretty self-explanitory. It simply
        refreshes all of the main windows.
        """

        self.screen.refresh()
        self.refresh_options()
        self.option_box.refresh()
        self.pack_info_box.refresh()
        self.opt_info_box.refresh()

    def get_selected_item(self, a_box):

        """ This function uses the current y-coordinate of the cursor
        to decide which item from the options list is selected.
        """
        # We do not need the x value, so a underscore is passed
        current_y, _ = a_box.getyx()
        #  Find the index by subtracting the height of the start of
        # the list, and the top of the window
        item_index = current_y - 4
        current_item = self.option_list[item_index]

        return current_item

    def get_option_values(self):

        """ This function returns the indices of the options selected
        using the interface, and returns them as a list.
        """

        return_list = []

        for item in self.option_dict:
            if self.option_dict[item]:
                return_list.append(self.option_list.index(item))
        # Return a version of the list that is sorted by value
        return sorted(return_list, key=int)

    def get_entry_values(self):

        """ This function returns a list of values entered by the
        user, specifically the package name and version which are
        entered at the beginning of the build.
        """

        returns = []

        for string in [self.package_name, self.package_version]:
            if isinstance(string, bytes):
                returns.append(string.decode('utf-8'))
            else:
                returns.append(string)

        return returns

    def main_loop(self):

        """ This is the main loop of the interface. It deals with
        a large majority of the user input.
        """

        pack_name = self.pack_info_box.getstr(2, 11, 22)[:18]
        pack_version = self.pack_info_box.getstr(3, 11, 22)[:18]

        curses.noecho()
        # If the line is left empty, display the default value
        if pack_name.decode('utf-8') == '':
            self.pack_info_box.addstr(2, 11, self.package_name)
        else:
            self.pack_info_box.addstr(2, 11, pack_name)
            self.package_name = pack_name

        if pack_version.decode('utf-8') == '':
            self.pack_info_box.addstr(3, 11, self.package_version)
        else:
            self.pack_info_box.addstr(3, 11, pack_version)
            self.package_version = pack_version
        # Add some more lines to the package info box
        self.pack_info_box.addstr(5, 2, 'DestDir:', curses.A_BOLD)
        self.pack_info_box.addstr(5, 11, '/usr/local/tadman')

        self.pack_info_box.addstr(6, 2, 'BldType:', curses.A_BOLD)
        self.pack_info_box.addstr(6, 11, self.build_type)

        self.refresh_main_screen()
        # Move the cursor to the start of the options list
        self.screen.move(4, 4)

        key = ''
        exit_interface = True
        # Read incoming keypresses until quit pr execute
        while exit_interface:

            key = self.screen.getch()
            current_y, current_x = self.screen.getyx()

            if key == ord('q'):
                exit_interface = False

            elif key == ord('e'):
                exit_interface = False

            elif key == curses.KEY_UP:
                if current_y > 4:
                    current_y -= 1

            elif key == curses.KEY_DOWN:
                if current_y < 3 + len(self.option_list):
                    current_y += 1

            elif key == ord('\n'):

                current_item = self.get_selected_item(self.screen)
                new_value = not self.option_dict[current_item]
                self.option_dict[current_item] = new_value

                self.refresh_options()
                self.option_box.refresh()

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
    IN_LIST = ['Enable verbose build', 'Enable unicode support',
               'Disable squid mode', 'Disable colored output']
    N_INTERFACE = CursesInterface(IN_LIST, 'squid', '1.4.18', 'autotools')
    if N_INTERFACE.main_loop():
        print(N_INTERFACE.get_option_values())
        print(N_INTERFACE.get_entry_values())
