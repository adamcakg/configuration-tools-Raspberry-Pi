import test.passwordpage as passwordpage
import test.softwarepage as softwarepage
from .handler import Handler

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class UpdatePage:
    def __init__(self):
        self.__builder = Gtk.Builder()                  # Initializing builder
        self.__builder.add_from_file('update_page/update_page.glade')   # creating object from XML(.glade files)

    def next(self, controller):
        controller.set_state(softwarepage.SoftwarePage())

    def back(self, controller):
        controller.set_state(passwordpage.PasswordPage())

    def get_xml_object(self):
        return self.__builder.get_object('update_page')

    def destroy(self):
        del self

    def connect_handler(self, controller):
        self.__builder.connect_signals(Handler(controller))

    def execute(self):
        pass
