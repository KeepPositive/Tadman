""" Welcome to the GTK+3 GUI interface for the Tadman package
manager! I'm really proud with how this is all turning out. But there
are a few tidbits I would like to improve still, like searching, and adding
values to options with an equals at the end.
"""

## Dependencies
import gi
gi.require_version('Gtk', '3.0')
import gi.repository.Gtk as Gtk

class MainInterface(Gtk.Window):

    """ This class is in charge of managing the GTK+ 3.0 based GUI for Tadman.
    It currently consists of two main parts: the options list with toggles on
    the left, and the 'information window' on the right. When closed, the
    script outputs all selected options, which will be sent to the build system
    being used.
    """

    def __init__(self, in_dict, pack_name, pack_version, mode):

        """ Initialize all of the internal and external parts of the GUI. """

        self.mode = mode
        self.options_dict = in_dict
        self.options_list = []
        for item in self.options_dict:
            self.options_list.append(item)

        self.toggle_list = []
        self.info_list = []

        dict_length = len(in_dict)
        self.list_range = range(dict_length)
        # Initialize GTK window and set a title
        Gtk.Window.__init__(self, title='Tadman Package Manager')
        # Set the perfect window dimensions, and make it non-resizable
        self.set_default_size(750, 500)
        self.set_resizable(False)
        self.connect("delete-event", Gtk.main_quit)

        # Initialize all containers going to be used
        notebook_window = Gtk.Notebook()
        main_box = Gtk.HBox()
        left_box = Gtk.VBox()
        right_box = Gtk.VBox()
        scrolly = Gtk.ScrolledWindow()
        button_box = Gtk.HBox()
        self.list_model = Gtk.ListStore(str, bool)
        self.tree_view = Gtk.TreeView(model=self.list_model, activate_on_single_click=True)
        #self.tree_view.connect('cursor-changed', self.change_help_message)

        # Initialize buttons and smaller things
        run_button = Gtk.Button(label='Run')
        cancel_button = Gtk.Button(label='Cancel')
        self.help_message = Gtk.Label("Welcome to Tadman!")
        self.package_name = Gtk.Entry()
        self.package_version = Gtk.Entry()
        #search_bar = Gtk.Entry()
        cell = Gtk.CellRendererText()
        toggle = Gtk.CellRendererToggle()
        for title in self.options_dict:
            # Add a line to the list_store for each option
            self.list_model.append([title, False])

        # Configure container(s)
        scrolly.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        column_one = Gtk.TreeViewColumn('Name', cell, text=0)
        column_two = Gtk.TreeViewColumn('Toggle', toggle, active=1)
        column_two.set_sizing(Gtk.TreeViewColumnSizing.FIXED)
        column_two.set_fixed_width(25)
        self.select = self.tree_view.get_selection()
        self.select.connect("changed", self.tree_selection_changed)
        # Note: Here are options for a search bar, but does not really work well
        self.tree_view.set_enable_search(False)
        #self.tree_view.set_search_column(0)
        #self.tree_view.set_search_entry(search_bar)

        # Configure button(s)
        run_button.connect('clicked', self.run_was_pressed)
        cancel_button.connect('clicked', self.cancel_was_pressed)
        toggle.connect('toggled', self.cell_was_toggled)
        self.help_message.set_line_wrap(True)
        self.help_message.set_width_chars(30)
        self.help_message.set_max_width_chars(30)
        self.help_message.set_justify(Gtk.Justification.CENTER)
        self.package_name.set_text(pack_name)
        self.package_version.set_text(pack_version)

        # Start placing containers in containers and widgets in containers.
        self.add(notebook_window)
        notebook_window.append_page(main_box, Gtk.Label('Config'))
        main_box.pack_start(left_box, True, True, 5)
        main_box.pack_start(right_box, True, False, 5)
        #left_box.pack_start(search_bar, False, False, 2)
        left_box.pack_start(scrolly, True, True, 0)
        left_box.pack_end(button_box, False, False, 2)
        button_box.pack_start(run_button, True, True, 4)
        button_box.pack_start(cancel_button, True, True, 4)
        self.tree_view.append_column(column_one)
        self.tree_view.append_column(column_two)
        scrolly.add(self.tree_view)
        right_box.pack_start(self.package_name, False, False, 1)
        right_box.pack_start(self.package_version, False, False, 1)
        right_box.pack_start(Gtk.Label("Number of options: %d" % dict_length),
                             False, False, 1)
        right_box.pack_start(self.help_message, False, False, 10)

    def cell_was_toggled(self, widget, path):

        """ Change the toggle switch's status when clicked. """

        self.list_model[path][1] = not self.list_model[path][1]

        option = int(path)
        # If this is a CMake build, then the option must have 'ON' appened to
        # the end of it

        if self.list_model[path][1]:
            self.toggle_list.append(option)
        else:
            # If already toggled and then un-toggled, remove item from list
            self.toggle_list.remove(option)

    def tree_selection_changed(self, selection):

        """ This one is kinda confusing, but essentially it gets the value of
        the current selection once it is change, and puts up it's help message
        on the right panel.
        """

        model, treeiter = selection.get_selected()
        if not treeiter is None:
            # It must loop through all of the entries in order to set the help
            # message, which I'm not very pleased with
            if model[treeiter][0] in self.options_dict:
                item = model[treeiter][0]
                self.help_message.set_text(self.options_dict[item][1])

    def run_was_pressed(self, widget):

        """ When the run button is hit, the current options in the name entry
        box and the toggle options selected are saved to a list, and the GUI
        closes.
        """
        Gtk.main_quit()

        self.info_list.append(self.package_name.get_text())
        self.info_list.append(self.package_version.get_text())
        #self.info_list.append(self.toggle_list)
        self.info_list.append(sorted(self.toggle_list, key=int))

    def cancel_was_pressed(self, widget):

        """ Similar to run_was_pressed, but sets all options to none, and
        then closes the GUI.
        """

        self.info_list = []

        Gtk.main_quit()

    def get_return_values(self):

        return self.info_list


def gui_main(mode, pack_name, pack_version, a_list):

    """ A main function to run the entire GUI. Nothing all that special."""

    window = MainInterface(mode, pack_name, pack_version, a_list)
    window.show_all()
    Gtk.main()

    window.hide()

    return window.get_return_info()


if __name__ == '__main__':
    # For testing purposes ;)
    OPTIONS = [['YOOO', '--enable-yo', "Enable native slang support in browser"],
               ['Squiddy', '--disable-squid', "Disable the standard Squiddy theme"]]
    GUI = gui_main('autotools', 'ted_test', '3.2.1', OPTIONS)
