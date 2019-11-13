import softwarepage as softwarepage
from .handler import Handler

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class AllSet:

    def __init__(self):
        self.__builder = Gtk.Builder()                  # Initializing builder
        self.__builder.add_from_file('allset/all_set.glade')   # creating object from XML(.glade files)

    def next(self, controller):
        pass

    def back(self, controller):
        controller.set_state(softwarepage.SoftwarePage())

    def get_xml_object(self):
        return self.__builder.get_object('all_set')

    def destroy(self):
        del self

    def connect_handler(self, controller):
        self.__builder.connect_signals(Handler(controller))
