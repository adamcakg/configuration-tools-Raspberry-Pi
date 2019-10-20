
import test.passwordpage as passwordpage
import test.welcome as welcome
from .handler import Handler

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class SettingsPage:

    def __init__(self):
        self.__builder = Gtk.Builder()                  # Initializing builder
        self.__builder.add_from_file('settings/settings.glade')   # creating object from XML(.glade files)

    def next(self, controller):
        controller.set_state(passwordpage.PasswordPage())

    def back(self, controller):
        controller.set_state(welcome.WelcomePage())

    def get_xml_object(self):
        return self.__builder.get_object('settings')

    def destroy(self):
        del self

    def connect_handler(self, controller):
        self.__builder.connect_signals(Handler(controller))
