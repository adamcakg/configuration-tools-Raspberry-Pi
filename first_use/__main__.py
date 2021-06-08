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
        
        size = Gdk.Screen.get_default()
        
        if size.get_width() <= 600 or size.get_height() <= 800:
            self.set_border_width(10)      
            self.set_resizable(True)
            self.fullscreen()
        else:
            self.set_decorated(False)
            self.set_keep_above(True)
            x = (size.get_width() - 500)/2
            y = (size.get_height() - 500)/2
            
            self.move(x, y)
        
            self.set_border_width(10)                           # Border all around window
            self.set_default_size(500, 500)                     # Setting default size of window
            self.set_resizable(False)
        
        controller.Controller(self)                                    # Giving control to controller class


# METHOD TO SET CSS STYLE
# ----------------------------------------------------------------------------------------------------------------------
def gtk_style():
        style_provider = Gtk.CssProvider()
        style_provider.load_from_path('/opt/first_use/css/style.css')
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), style_provider,
                                                 Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

if __name__ == '__main__':
    settings_thread = threading.Thread(target=settings_stuff.do_thread())
    timezone_thread = threading.Thread(target=timezone.do_threading())

    settings_thread.start()
    timezone_thread.start()

    gtk_style()
    win = FirstStart()                                          # Starting app
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()                                                  # App loop
