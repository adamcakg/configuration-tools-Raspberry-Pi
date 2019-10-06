import gi
from list_of_pages import pages
from handler import Handler

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio




class FirstStart(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Welcome")
        self.set_border_width(10)
        self.set_default_size(400, 200)
        # self.fullscreen()

        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.set_transition_duration(1000)
        self.add(self.stack)

        self.builder = Gtk.Builder()

        for page in pages:
            self.builder.add_from_file('glade/{}.glade'.format(page))
            self.builder.connect_signals(Handler(self.stack))
            variable = self.builder.get_object(page)
            self.stack.add_named(variable, page)



        # builder.add_from_file("glade/welcome.glade")
        #
        #
        #
        # welcome_box = builder.get_object("welcome_box")
        #
        # self.stack.add_named(welcome_box, 'welcome_box')
        #
        # box1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        # label = Gtk.Label("first page")
        # self.button = Gtk.Button(label="next")
        # self.button.connect("clicked", self.button_clicked1)
        # box1.add(label)
        # box1.add(self.button)
        #
        # box2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        # label = Gtk.Label("second page")
        # self.button = Gtk.Button(label="next")
        # self.button.connect("clicked", self.button_clicked2)
        # box2.add(label)
        # box2.add(self.button)
        #
        # self.stack.add_named(box1, 'box1')
        # self.stack.add_named(box2, 'box2')




    # def button_clicked1(self, widget):
    #     self.stack.set_visible_child_name('page2')

    # def button_clicked2(self, widget):
    #     self.stack.set_visible_child_name('box1')

win = FirstStart()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()