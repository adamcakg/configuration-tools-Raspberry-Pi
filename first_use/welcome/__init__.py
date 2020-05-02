import settings as settings
import random
from .handler import Handler
from page import Page

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib


class WelcomePage(Page):
    def __init__(self):
        self.builder = Gtk.Builder()                  # Initializing builder
        self.builder.add_from_file('/etc/first_use/welcome/welcome.glade')   # creating object from XML(.glade files)

        self.list_of_welcomes = ['Welcome', 'Vitajte', 'Willkommen', 'Bienvenidos', 'Bienvenue', 'أهلا بك']
        self.previous = 'Welcome'
        self.label = self.builder.get_object('welcome_label')
        self.execute()

# METHOD TO GO NEXT
# ----------------------------------------------------------------------------------------------------------------------
    def next(self, controller):
        controller.set_state(settings.SettingsPage())

# METHOD TO GO BACK
# ----------------------------------------------------------------------------------------------------------------------
    def back(self, controller):
        return

# METHOD TO GET XML OBJECT
# ----------------------------------------------------------------------------------------------------------------------
    def get_xml_object(self):
        return self.builder.get_object('welcome')

# METHOD TO DESTROY ITSELF
# ----------------------------------------------------------------------------------------------------------------------
    def destroy(self):
        del self

# METHOD TO SET RANDOM WELCOME TEXT LABEL ON SCREEN
# ----------------------------------------------------------------------------------------------------------------------
    def get_random_welcome_text(self):
        label = random.choice(self.list_of_welcomes)

        while label == self.previous:
            label = random.choice(self.list_of_welcomes)

        self.previous = label
        self.label.set_label(label)
        GLib.timeout_add_seconds(3, self.get_random_welcome_text)

# METHOD TO CONNECT HANDLER
# ----------------------------------------------------------------------------------------------------------------------
    def connect_handler(self, controller):
        self.builder.connect_signals(Handler(controller))

# METHOD TO EXECUTE PAGE
# ----------------------------------------------------------------------------------------------------------------------
    def execute(self):
        GLib.timeout_add_seconds(3, self.get_random_welcome_text)
