""" Welcome to the Tadman ncurses interface. It's original goal was
to have all the functionality of the GTK+ version, but use fewer
dependencies and be accessible from a terminal interface.

Now, this interface is the main interface of the project. The GTK+
variant will be updated later on if anyone shows interest in using it.
"""

# Standard
import curses
import datetime
import sys
import textwrap

class MainInterface():

    """ This is the class for the Tadman curses interface. It is
    relatively simple, but still retains a large amount of
    functionality.
    """

    def __init__(self, opt_dict, inst_dict):

        # Initialize some global variables
        self.option_dict = opt_dict
        self.package_name = ''
        self.package_version = ''
        self.build_type = ''
        self.window = 'build'
        self.option_list = []
        self.install_list = []
        self.toggle_dict = {}
        self.install_toggle = {}
        self.install_dict = inst_dict
        self.options_avail = 0
        self.install_avail = 0

        for item in self.option_dict:
            self.option_list.append(item)
            self.toggle_dict[item] = False
            self.options_avail += 1

        for item in self.install_dict:
            self.install_list.append(item)
            self.install_toggle[item] = [False, '']
            self.install_avail += 1

        # Initalize the screen
        self.screen = curses.initscr()

        # Check if screen is large enough
        max_y, max_x = self.screen.getmaxyx()
        if max_y < 24 or max_x < 80:
            curses.endwin()
            print("Terminal must be at least 24 rows by 80 columns")
            print("It is currently {} rows by {} columns".format(max_y, max_x))
            sys.exit(0)

        # Prepare the main screen
        curses.echo()
        curses.cbreak()
        self.screen.keypad(1)
        # Add a title to the main screen
        self.screen.addstr(0, 1, "Tadman Package Manager", curses.A_UNDERLINE)
        # Add a small help message that will be covered up later
        self.screen.addstr(14, 41, "NOTE: If no value is entered,")
        self.screen.addstr(15, 41, "the default will be selected")

        # Start initializing subwindows
        # Create a sub window that will contain the options list
        self.option_box = curses.newwin(20, 36, 2, 0)
        # Create a pad window for the actual options list
        self.option_pad = curses.newpad(self.options_avail + 4, 36)

        # Create a sub window for package information
        self.pack_info_box = curses.newwin(9, 44, 2, 36)
        # Create a sub window for option information
        self.opt_info_box = curses.newwin(11, 44, 11, 36)

        # A box for install flag options
        self.install_flag_box = curses.newwin(20, 36, 2, 0)
        # Make a pad for this scrollable list as well
        self.install_pad = curses.newpad(self.install_avail + 4, 36)
        self.install_info = curses.newwin(11, 44, 11, 36)

        # Add a text wrapper for convinence
        self.wrapper = textwrap.TextWrapper(width=40)

    def init_package_info_entry(self):

        """ Once the script begins, it is a good idea to run this
        function. It allows the user to enter vital package info
        easily and efficiently.
        """

        # Add some title lines
        self.pack_info_box.box()
        self.pack_info_box.addstr(0, 1, 'Package Info')
        # Add some titles
        self.pack_info_box.addstr(2, 2, "Package:", curses.A_BOLD)
        self.pack_info_box.addstr(3, 2, "Version:", curses.A_BOLD)
        self.pack_info_box.addstr(4, 2, 'DestDir:', curses.A_BOLD)
        self.pack_info_box.addstr(5, 2, 'FldName:', curses.A_BOLD)
        self.pack_info_box.addstr(6, 2, 'BldType:', curses.A_BOLD)

        # Now we begin the program
        self.screen.refresh()
        # Get some user input
        default_pack =  "Default value: {}".format(self.package_name)
        self.screen.addstr(12, 41, default_pack)
        self.screen.refresh()
        pack_name = self.pack_info_box.getstr(2, 11, 27).decode('utf-8')

        self.screen.addstr(12, 41, ' ' * 40)
        # If version number was found, default to a datetime string
        if self.package_version == '':
            time_now = datetime.datetime.now()
            self.package_version = time_now.strftime('%y%m%d%H%M%S')

        default_version = "Default value: {}".format(self.package_version)
        self.screen.addstr(12, 41, default_version)
        self.screen.refresh()
        pack_version = self.pack_info_box.getstr(3, 11, 27).decode('utf-8')
        # Disable the users ability to type freely
        curses.noecho()
        # If the line is left empty, set variable to the default value
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
        # Print a little help message
        self.screen.addstr(22, 30, "Hit '?' for help")
        self.screen.refresh()

    def refresh_install_flag_list(self):

        """ When the user selects a flag, an X will appear. This works
        because of this function.
        """

        offset_y = 0

        for item in self.install_list:
            if self.build_type == 'autotools':
                display_item = item[2:-1]
            elif self.build_type == 'cmake':
                display_item = item.lower()

            if self.install_toggle[item][0]:
                self.install_pad.addstr(offset_y, 0, "[X] {}".format(display_item))
            else:
                self.install_pad.addstr(offset_y, 0, "[ ] {}".format(display_item))

            offset_y += 1

        self.install_flag_box.refresh()

    def refresh_options_list(self):

        """ This quaint little function reads the option dictionary,
        and prints out checkboxes according to whether the value is
        True or False.
        """

        offset_y = 0
        # For each item, print an X or not depending on the current state
        for item in self.option_list:
            value = self.toggle_dict[item]
            if value:
                if value == True:
                    character = 'X'
                    self.option_pad.addstr(offset_y, 0, "[X] %s" % item)
                elif value == 'ON':
                    character = 'Y'
                elif value == 'OFF':
                    character = 'N'
            else:
                character = ' '

            display = "[{}] {}".format(character, item)
            self.option_pad.addstr(offset_y, 0, display)

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
        wrapped_help_message = self.wrapper.wrap(original_help_message)

        pretty_index = str(index + 1).zfill(2)
        pretty_total = str(self.options_avail).zfill(2)
        self.opt_info_box.addstr(2, 16,
                                 "%s/%s" % (pretty_index, pretty_total))

        if self.build_type == 'cmake':
            option_flag = option_flag[2:-6]

        self.opt_info_box.addstr(3, 8, option_flag)

        message_height = 5
        for a_line in wrapped_help_message:
            self.opt_info_box.addstr(message_height, 2, str(a_line))
            message_height += 1

        self.opt_info_box.refresh()

    def refresh_install_info_box(self, index):

        """ While moving the cursor up and down within the interface,
        the option info box must be updated with information pertinent
        to the highlighted item. In order to keep these all in track
        and make the main_loop function slightly cleaner, this function
        updates the information by itself. Prior to writing, it also
        overwrites old info with whitespace.
        """

        current_item = self.install_list[index]

        # Overwrite old info with spaces
        self.install_info.addstr(2, 16, ' ' * 5)
        self.install_info.addstr(3, 11, ' ' * 27)
        self.install_info.addstr(4, 9, ' ' * 27)

        for line_y in [6, 7]:
            self.install_info.addstr(line_y, 2, ' ' * 40)

        # Gather and print out new information
        description, default_path = self.install_dict[current_item]
        wrapped_description = self.wrapper.wrap(description)
        pretty_index = str(index + 1).zfill(2)
        pretty_total = str(self.install_avail).zfill(2)

        self.install_info.addstr(2, 16,
                                 "%s/%s" % (pretty_index, pretty_total))
        self.install_info.addstr(3, 11, default_path)
        self.install_info.addstr(4, 9, self.install_toggle[current_item][1])

        description_height = 6
        for a_line in wrapped_description:
            self.install_info.addstr(description_height, 2, a_line)
            description_height += 1

        self.install_info.refresh()


    def refresh_option_windows(self):

        """ This method is pretty self-explanitory. It simply
        refreshes all of the main windows that have to do with
        choosing options.
        """

        self.refresh_options_list()
        self.option_box.refresh()
        self.opt_info_box.refresh()
        self.pack_info_box.refresh()
        self.screen.refresh()

    def refresh_install_windows(self):

        """ Update all of the install windows. Duh."""

        self.refresh_install_flag_list()
        self.refresh_install_info_box()
        self.pack_info_box.refresh()

    def get_return_values(self):

        """ This function returns all of the valuable information
        gathered by the GUI in the format of:

        [package_name, package_version, [optional_features], [install_flags]]
        """

        return_list = []
        option_list = []
        install_list = []

        for string in [self.package_name, self.package_version]:
            return_list.append(string)

        for item in self.toggle_dict:
            flag = self.option_dict[item][0]
            if self.build_type in ['autotools', 'autogen']:
                value = self.toggle_dict[item]
                if value:
                    option_list.append(flag)
            elif self.build_type == 'cmake':
                value = self.toggle_dict[item]
                if value:
                    option_flag = "{}{}".format(flag, value)
                    option_list.append(option_flag)

        for item in self.install_toggle:
            if self.install_toggle[item][0]:
                value = self.install_toggle[item][1]
                if self.build_type in ['autotools', 'autogen']:
                    full_flag = "{}{}".format(item, value)
                elif self.build_type == 'cmake':
                    full_flag = "-D{}:PATH={}".format(item, value)

                install_list.append(full_flag)

        return [self.package_name, self.package_version, option_list,
                install_list]

    def run_help_loop(self, previous_window):

        # Create a help message box
        help_box = curses.newwin(15, 78, 4, 1)
        help_box.box()
        help_box.addstr(0, 1, ' Help ')
        curses.curs_set(0)

        help_dict = {
                'General': [2, 2,
                            [('q', 'Quit tadman'),
                             ('e', 'Exec build w/ settings'),
                             ('?', 'Open/Close help window'),
                             ('ENTER', 'Select/Deselect option')]],
                'Selection': [8, 2,
                              [('UP', 'Scroll up one'),
                               ('DOWN', 'Scroll down one'),
                               ('HOME', 'Scroll to top'),
                               ('END', 'Scroll to bottom')]],
                'Autotools Build': [2, 36,
                                    [('RIGHT', 'Enter install flag select')]],
                'Install Flags': [11, 36,
                                  [('LEFT', 'Return to option selection')]],
                'CMake Build': [5, 36,
                                [('y', 'Activate feature'),
                                 ('n', 'Disable feature'),
                                 ('ENTER', 'Clear feature'),
                                 ('RIGHT', 'Enter install flag select')]]
        }

        for item in help_dict:
            y_set, x_set, sub_messages = help_dict[item]
            y_offset = 1

            help_box.addstr(y_set, x_set, item, curses.A_BOLD)

            y_set += 1
            x_set += 1

            for subitem in sub_messages:
                message_space = ' ' * (8 - len(subitem[0]))
                message = "{}{}{}".format(subitem[0], message_space,
                                          subitem[1])
                help_box.addstr(y_set, x_set, message)
                y_set += 1

        help_box.refresh()

        key = ''
        exit_main = False
        build_package = False

        while True:

            key = self.screen.getch()

            if key == ord('?'):
                break
            elif key == ord('e'):
                build_package = True
                exit_main = True
                break
            elif key == ord('q'):
                exit_main = True
                break

        curses.curs_set(1)
        self.window = previous_window

        return exit_main, build_package

    def run_option_loop(self):

        """ This loop allows the user to interact with the optional
        feature list and turn them on.
        """

        self.pack_info_box.box()
        self.pack_info_box.addstr(0, 1, 'Package Info')
        self.pack_info_box.refresh()

        # Set up the option info box for feature options
        self.opt_info_box.box()
        self.opt_info_box.addstr(0, 1, 'Option Info')
        self.opt_info_box.addstr(2, 2, "Option index:", curses.A_BOLD)
        self.opt_info_box.addstr(3, 2, "Flag:", curses.A_BOLD)
        self.opt_info_box.addstr(4, 2, "Help Message:", curses.A_BOLD)
        # If there are more options than available, indicate it
        self.option_box.addstr(1, 13, ' ' * 8)
        if self.options_avail > 15:
            self.option_box.addstr(18, 13, "▼ More ▼", curses.A_BOLD)

        # Initialize the info in the option info box
        self.refresh_option_info_box(0)
        self.refresh_option_windows()
        # Set up the box where options will be chosen
        self.option_box.box()
        self.option_box.addstr(0, 1, 'Option List')
        self.option_box.refresh()
        self.option_pad.refresh(0, 0, 4, 2, 19, 34)
        # Move the cursor to the start of the options list
        self.screen.move(4, 3)

        key = ''

        exit_main = False
        build_package = False
        pad_offset = 0
        window_offset = 4
        index_offset = window_offset + pad_offset
        maximum_offset = self.options_avail - 16
        maximum_y = self.options_avail + 3
        # Read incoming keypresses until quit or execute
        while not exit_main:

            key = self.screen.getch()
            current_y, current_x = self.screen.getyx()
            current_index = current_y - index_offset

            # When 'q'  or 'e' is pressed, close window
            if key == ord('e'):
                build_package = True
                exit_main = True
                break
            elif key == ord('q'):
                exit_main = True
                break
            elif key == ord('?'):
                self.window = 'build-help'
                break
            # When the up arrow is pressed, reduce y-value or scroll list up
            elif key == curses.KEY_UP:
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
            # Change modes if right is hit
            elif key == curses.KEY_RIGHT:
                self.window = 'install'
                break

            current_index = current_y + pad_offset - window_offset

            #  If 'enter' is pressed, add an X to the option by altering a
            # dictionary and refreshing the interface
            if key in [ord('y'), ord('n'), ord('\n')]:
                current_item = self.option_list[current_index]
                #print("KEYS")
                if self.build_type in ['autotools', 'autogen']:
                    if key == ord('\n'):
                        new_value = not self.toggle_dict[current_item]

                elif self.build_type == 'cmake':
                    if key == ord('y'):
                        new_value = 'ON'
                    elif key == ord('n'):
                        new_value = 'OFF'
                    elif key == ord('\n'):
                        new_value = False

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

        return exit_main, build_package

    def run_install_loop(self):

        """ This run loop is where the user is able to choose where
        certain things will be installed using install flags like
        '--mandir=' and things of that sort.
        """
        self.pack_info_box.box()
        self.pack_info_box.addstr(0, 1, 'Package Info')
        self.pack_info_box.refresh()

        # Set up the menu
        self.install_flag_box.box()
        self.install_flag_box.addstr(0, 1, 'Install Flags')
        self.install_flag_box.refresh()
        self.refresh_install_flag_list()
        self.install_pad.refresh(0, 0, 4, 2, 19, 34)

        self.install_info.box()
        self.install_info.addstr(0, 1, 'Install Flag Info')
        self.install_info.addstr(2, 2, 'Option Index: ', curses.A_BOLD)
        self.install_info.addstr(3, 2, 'Default: ', curses.A_BOLD)
        self.install_info.addstr(4, 2, 'Value: ', curses.A_BOLD)
        self.install_info.addstr(5, 2, 'Explaination: ', curses.A_BOLD)
        self.refresh_install_info_box(0)

        if self.install_avail > 15:
            self.install_flag_box.addstr(18, 13, "▼ More ▼", curses.A_BOLD)
            self.install_flag_box.refresh()

        self.screen.move(4, 3)
        self.screen.refresh()

        key = ''

        exit_main = False

        pad_offset = 0
        window_offset = 4
        index_offset = window_offset + pad_offset
        maximum_offset = self.install_avail - 16
        maximum_y = self.install_avail + 3

        while not exit_main:

            key = self.screen.getch()
            current_y, current_x = self.screen.getyx()
            current_index = current_y + pad_offset - window_offset
            build_package = False

            if key == ord('e'):
                build_package = True
                exit_main = True
                break
            elif key == ord('q'):
                print('exiting')
                exit_main = True
                break
            elif key == ord('?'):
                self.window = 'install-help'
                break
            elif key == curses.KEY_LEFT:
                self.window = 'build'
                break
            elif key == curses.KEY_UP:
                if current_y == 4 and pad_offset > 0:
                    pad_offset -= 1
                elif current_y > 4:
                    current_y -= 1
            elif key == curses.KEY_DOWN:
                if current_y == 19 and pad_offset < maximum_offset:
                    pad_offset += 1
                elif current_y < 19 and current_y < maximum_y:
                    current_y += 1
            elif key == ord('\n'):
                current_item = self.install_list[current_index]
                new_value = not self.install_toggle[current_item][0]
                self.install_toggle[current_item][0] = new_value
                offset_x = 6 + len(current_item)
                if new_value:
                    curses.echo()
                    value = self.install_info.getstr(4, 9, 30).decode('utf-8')
                    curses.noecho()
                    if value != '':
                        self.install_toggle[current_item][1] = value
                else:
                    self.install_toggle[current_item][1] = ''

            current_index = current_y + pad_offset - window_offset

            self.refresh_install_info_box(current_index)
            self.refresh_install_flag_list()
            self.install_pad.refresh(pad_offset, 0, 4, 2, 19, 34)

            if pad_offset > 0:
                self.install_flag_box.addstr(1, 13, "▲ More ▲", curses.A_BOLD)
            else:
                self.install_flag_box.addstr(1, 13, ' ' * 8)

            if pad_offset < maximum_offset:
                self.install_flag_box.addstr(18, 13, "▼ More ▼", curses.A_BOLD)
            else:
                self.install_flag_box.addstr(18, 13, ' ' * 8)

            self.install_flag_box.refresh()

            self.screen.move(current_y, current_x)
            self.screen.refresh()

        return exit_main, build_package

def main_loop(a_dict, inst_dict, name, version, build_type):

    """ This is a simple function with the goal of making scripts that
    utilize this interface more clean. It sets all of the vital info,
    and runs all of the major loops available in a specific order.
    """

    interface = MainInterface(a_dict, inst_dict)

    interface.package_name = name
    interface.package_version = version
    interface.build_type = build_type

    interface.init_package_info_entry()

    exit_main = False

    while not exit_main:
        if interface.window == 'build':
            exit_main, build_package = interface.run_option_loop()
        elif interface.window == 'install':
            exit_main, build_package = interface.run_install_loop()
        elif interface.window == 'build-help':
            exit_main, build_package = interface.run_help_loop('build')
        elif interface.window == 'install-help':
            exit_main, build_package = interface.run_help_loop('install')

    curses.endwin()

    if build_package:
        return interface.get_return_values()
    else:
        return False
