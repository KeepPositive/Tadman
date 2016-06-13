#! /usr/bin/python3

import gi
gi.require_version('Gtk', '3.0')
import gi.repository.Gtk as Gtk

class InstallGtkGui(Gtk.Window):

    def __init__(self):

        self.install_choice = ()
        self.command = command_to_run

        Gtk.Window.__init__(self, title="Install?")

        self.set_default_size(300, 100)
        self.set_resizable(False)
        self.connect("delete-event", Gtk.main_quit)

        main_box = Gtk.VBox()
        button_box = Gtk.HBox() 
        
        intro_label = Gtk.Label("Would you like to install?")
        install_button = Gtk.Button(label='Install')
        cancel_button = Gtk.Button(label='Cancel')

        install_button.connect('clicked', self.install_was_pressed)
        cancel_button.connect('clicked', self.cancel_was_pressed)
       
        self.add(main_box)
        button_box.pack_start(install_button, True, True, 5)
        button_box.pack_start(cancel_button, True, True, 5)

        main_box.pack_start(intro_label, True, True, 0)
        main_box.pack_start(button_box, True, True, 5)


    def install_was_pressed(self, widget):
        
        self.install_choice = True

        Gtk.main_quit()

    def cancel_was_pressed(self, widget):

        self.install_choice = False

        Gtk.main_quit()

    def get_choice():

        return self.install_choice

if __name__ == '__main__':
    window = InstallGtkGui()
    window.show_all()
    Gtk.main()

