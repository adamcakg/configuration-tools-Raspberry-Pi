from gi.repository import Gtk

class Handler:
    def __init__(self, stack):
        self.stack = stack

    def onDestroy(self, *args):
        Gtk.main_quit()

    def next(self, button):
        self.stack.set_visible_child_name('page2')

    def back(self, button):
        self.stack.set_visible_child_name('welcome')