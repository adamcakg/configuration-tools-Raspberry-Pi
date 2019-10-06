import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gio


class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="HeaderBar Demo")

        hb = Gtk.HeaderBar()
        hb.props.title = "HeaderBar example"
        self.set_titlebar(hb)

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(box.get_style_context(), "linked")

        button = Gtk.Button()
        button.add(Gtk.Arrow(Gtk.ArrowType.LEFT, Gtk.ShadowType.NONE))
        box.add(button)

        button = Gtk.Button()
        button.add(Gtk.Arrow(Gtk.ArrowType.RIGHT, Gtk.ShadowType.NONE))
        box.add(button)

        hb.pack_start(box)

        # Stack - container that shows one item at a time
        main_area = Gtk.Stack()
        main_area.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        main_area.set_transition_duration(10)

        # Check box
        check_button = Gtk.CheckButton("Do not fn check me")
        main_area.add_titled(check_button, "checkbox_name", "Check Box")

        # Label
        label = Gtk.Label()
        label.set_markup("<big>OMG this text is huge!</big>")
        main_area.add_titled(label, "label_name", "Big Label")

        # StackSwitcher - controller for the stack (row of buttons you can click to change items)
        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(main_area)

        box1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(box1)
        box1.pack_start(stack_switcher, True, True, 0)
        box1.pack_start(main_area, True, True, 0)



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






win = MainWindow()
win.fullscreen()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
