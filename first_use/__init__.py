import gi
import controller as controller

import threading
from time import sleep

from settings import settings_stuff
from settings import timezone

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk


class FirstStart(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Welcome")          # Constructor to Gtk.window
        self.set_border_width(10)                           # Border all around window
        self.set_default_size(600, 600)                     # Setting default size of window
        #self.set_resizable(False)                           # Setting window to not be resizable
        #self.fullscreen()
        
        controller.Controller(self)                                    # Giving control to controller class


# METHOD TO SET CSS STYLE
# ----------------------------------------------------------------------------------------------------------------------
def gtk_style():
        style_provider = Gtk.CssProvider()
        style_provider.load_from_path('css/style.css')
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), style_provider,
                                                 Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

settings_thread = threading.Thread(target=settings_stuff.do_thread())
timezone_thread = threading.Thread(target=timezone.do_threading())

settings_thread.start()
timezone_thread.start()

gtk_style()
win = FirstStart()                                          # Starting app
win.show_all()
Gtk.main()                                                  # App loop
