import gi
from handler import Handler

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio


class Settings(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Welcome")
        self.set_border_width(10)
        self.set_default_size(600, 200)
        # TODO --

        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.set_transition_duration(500)
        self.add(self.stack)

        self.builder = Gtk.Builder()

        for index in range(len(pages)):
            self.builder.add_from_file('glade/{}.glade'.format(pages[index]))
            self.builder.connect_signals(Handler(self.stack, position=index))
            variable = self.builder.get_object(pages[index])
            self.stack.add_named(variable, pages[index])


win = Settings()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
