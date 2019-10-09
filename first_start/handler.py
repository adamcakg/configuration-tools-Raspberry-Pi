import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Handler:
    def __init__(self, controller, name_of_class=None):
        self.controller = controller                                # Handlers controls only one controller
        self.name = name_of_class

    def on_destroy(self, *args):                                    # Closing app
        print('quiting of ' + self.name)
        Gtk.main_quit()
        # del self

    def next(self, button):                                         # Button handler to get to next page
        self.controller.next_page()

    def back(self, button):                                         # Button handler to get to previous page
        self.controller.prev_page()
