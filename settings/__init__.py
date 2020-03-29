import gi
import controller

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib

class Settings(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Welcome")          # Constructor to Gtk.window
                                   # Setting window to not be resizable
        size = Gdk.Screen.get_default()
        
        self.set_default_size(600, 310)
        x = (size.get_width() - 600)/2
        y = (size.get_height() - 310)/2
        self.move(x, y)
        self.set_resizable(False)
        
        self.set_icon_from_file('img/icon.svg')
        
        controller.Controller(self)                                    # Giving control to controller class


def gtk_style():
        style_provider = Gtk.CssProvider()
        style_provider.load_from_path('css/style.css')
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), style_provider,
                                                 Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)


gtk_style()

win = Settings()                                          # Starting app
win.connect("destroy", Gtk.main_quit)
win.show_all()

Gtk.main()                                                  # App loop


