import test.update_page as update_page
import test.allset as allset
from .handler import Handler

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class SoftwarePage:
    def __init__(self):
        self.__builder = Gtk.Builder()                  # Initializing builder
        self.__builder.add_from_file('softwarepage/software_page.glade')   # creating object from XML(.glade files)

    def next(self, controller):
        controller.set_state(allset.AllSet())

    def back(self, controller):
        controller.set_state(update_page.UpdatePage())

    def get_xml_object(self):
        return self.__builder.get_object('software_page')

    def destroy(self):
        del self

    def connect_handler(self, controller):
        self.__builder.connect_signals(Handler(controller))