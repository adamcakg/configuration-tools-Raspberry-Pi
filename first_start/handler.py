from gi.repository import Gtk
from list_of_pages import pages


class Handler:
    def __init__(self, stack, position):
        self.stack = stack
        self.position = position

    def on_destroy(self, *args):
        Gtk.main_quit()

    def next(self, button):
        position = self.position + 1
        if position > len(pages):
            return
        else:
            self.stack.set_visible_child_name(pages[position])

    def back(self, button):
        position = self.position - 1
        if position < 0:
            return
        else:
            self.stack.set_visible_child_name(pages[position])
