import settings as settings
import random
from .handler import Handler

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib


class WelcomePage:
    def __init__(self):
        self.__builder = Gtk.Builder()                  # Initializing builder
        self.__builder.add_from_file('welcome/welcome.glade')   # creating object from XML(.glade files)

        self.__list_of_welcomes = ['Welcome', 'Vitajte', 'Willkommen', 'Bienvenidos', '어서 오세요', 'Bienvenue', 'أهلا بك']
        self.__previous = 'Welcome'
        self.__label = self.__builder.get_object('welcome_label')
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
        return self.__builder.get_object('welcome')

# METHOD TO DESTROY ITSELF
# ----------------------------------------------------------------------------------------------------------------------
    def destroy(self):
        del self

# METHOD TO SET RANDOM WELCOME TEXT LABEL ON SCREEN
# ----------------------------------------------------------------------------------------------------------------------
    def __get_random_welcome_text(self):
        label = random.choice(self.__list_of_welcomes)

        while label == self.__previous:
            label = random.choice(self.__list_of_welcomes)

        self.__previous = label
        self.__label.set_label(label)
        GLib.timeout_add_seconds(3, self.__get_random_welcome_text)

# METHOD TO CONNECT HANDLER
# ----------------------------------------------------------------------------------------------------------------------
    def connect_handler(self, controller):
        self.__builder.connect_signals(Handler(controller))

# METHOD TO EXECUTE PAGE
# ----------------------------------------------------------------------------------------------------------------------
    def execute(self):
        GLib.timeout_add_seconds(3, self.__get_random_welcome_text)
