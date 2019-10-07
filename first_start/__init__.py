import gi
from list_of_pages import pages
from list_of_welcomes import Welcomes
from handler import Handler

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GLib


class FirstStart(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Welcome")
        self.set_border_width(10)
        self.set_default_size(400, 200)
        # self.fullscreen()

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

        welcome_label = self.builder.get_object("welcome_label")
        welcomes = Welcomes(welcome_label, self)


win = FirstStart()
win.show_all()
Gtk.main()
