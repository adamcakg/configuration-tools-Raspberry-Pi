import gi
from controller import Controller

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class FirstStart(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Welcome")          # Constructor to Gtk.window
        self.set_border_width(10)                           # Border all around window
        self.set_default_size(400, 200)                     # Setting default size of window
        self.set_resizable(False)                           # Setting window to not be resizable
        # self.fullscreen()

        Controller(self)                                    # Giving control to controller class


win = FirstStart()                                          # Starting app
win.show_all()
Gtk.main()                                                  # App loop
