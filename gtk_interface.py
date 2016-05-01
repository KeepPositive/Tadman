""" Welcome to the first (And only) GUI interface for the Tadman package
manager! I'm really proud with how this is all turning out. But there
are a few tidbits I would like to improve still, like searching, and adding
values to options with an equals at the end.
"""

import gi
gi.require_version('Gtk', '3.0')
import gi.repository.Gtk as Gtk

class TadmanGtkGui(Gtk.Window):

    """ This class is in charge of managing the GTK+ 3.0 based GUI for Tadman.
    It currently consists of two main parts: the options list with toggles on
    the left, and the 'information window' on the right. When closed, the
    script outputs all selected options, which will be sent to the build system
    being used.
    """

    def __init__(self, mode, in_list):

        """ Initialize all of the internal and external parts of the GUI. """

        self.mode = mode
        self.options_list = in_list
        self.toggle_list = []
        self.entry_list = []

        list_length = len(in_list)
        self.list_range = range(list_length)
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
        self.list_model = Gtk.ListStore(str, bool)
        self.tree_view = Gtk.TreeView(model=self.list_model, activate_on_single_click=True)
        #self.tree_view.connect('cursor-changed', self.change_help_message)

        # Initialize buttons and smaller things
        run_button = Gtk.Button(label='Run')
        self.help_message = Gtk.Label("Welcome to Tadman!")
        #search_bar = Gtk.Entry()
        cell = Gtk.CellRendererText()
        toggle = Gtk.CellRendererToggle()
        for index in self.list_range:
            # Add a line to the list_store for each option
            self.list_model.append([self.options_list[index][0], False])

        # Configure container(s)
        scrolly.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        column_one = Gtk.TreeViewColumn('Name', cell, text=0)
        column_two = Gtk.TreeViewColumn('Toggle', toggle, active=1)
        column_two.set_sizing(Gtk.TreeViewColumnSizing.FIXED)
        column_two.set_fixed_width(25)
        self.select = self.tree_view.get_selection()
        self.select.connect("changed", self.tree_selection_changed)
        # Options for a search bar, but does not really work well
        #self.tree_view.set_enable_search(True)
        #self.tree_view.set_search_column(0)
        #self.tree_view.set_search_entry(search_bar)

        # Configure button(s)
        run_button.connect('clicked', self.run_options)
        toggle.connect('toggled', self.cell_was_toggled)
        self.help_message.set_line_wrap(True)
        self.help_message.set_width_chars(30)
        self.help_message.set_max_width_chars(30)

        # Start placing containers in containers and widgets in containers.
        self.add(notebook_window)
        notebook_window.append_page(main_box, Gtk.Label('Config'))
        main_box.pack_start(left_box, True, True, 5)
        main_box.pack_start(right_box, True, False, 5)
        #left_box.pack_start(search_bar, False, False, 2)
        left_box.pack_start(scrolly, True, True, 0)
        left_box.pack_end(run_button, False, False, 0)
        self.tree_view.append_column(column_one)
        self.tree_view.append_column(column_two)
        scrolly.add(self.tree_view)
        right_box.pack_start(Gtk.Label("Number of options: %d" % list_length), False, False, 1)
        right_box.pack_start(self.help_message, False, False, 5)

    def cell_was_toggled(self, widget, path):

        """ Change the toggle switch's status when clicked. """

        self.list_model[path][1] = not self.list_model[path][1]

        option = self.options_list[int(path)][1]
        # If this is a CMake build, then the option must have 'ON' appened to
        # the end of it
        if self.mode == 'cmake':
            option = "%s%s" % (option, 'ON')

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
            for index in self.list_range:
                if model[treeiter][0] in self.options_list[index]:
                    self.help_message.set_text(self.options_list[index][2])

    def run_options(self, widget):

        """ When the run button is hit, the GUI closes, and the list of options
        is set in a variable.
        """

        Gtk.main_quit()

    def get_toggle_values(self):

        """ Retrieve the toggled value list, consisting of options check off
        just before the GUI closed.
        """

        return self.toggle_list



def gui_main(mode, a_list):

    """ A main function to run the entire GUI. Nothing all that special."""

    window = TadmanGtkGui(mode, a_list)
    window.show_all()
    Gtk.main()

    return window.get_toggle_values()


if __name__ == '__main__':
    # For testing purposes ;)
    OPTIONS = [['YOOO', '--enable-yo', "Enable native slang support in browser"],
               ['Squiddy', '--disable-squid', "Disable the standard Squiddy theme"]]
    print(TadmanGtkGui('autotools', OPTIONS))
