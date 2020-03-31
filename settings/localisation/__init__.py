import gi
from .handler import Handler
from page import Page

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Localisation(Page):
    def __init__(self):
        self.name = 'Localisation'
        self.__builder = None
        self.handler = None
        self.header = None

    def get_xml_object(self):
        return self.__builder.get_object('localisation')

    def destroy(self):
        del self
        
    def connect_builder(self):
        self.__builder = Gtk.Builder()  # Initializing builder
        self.__builder.add_from_file('/etc/settings/localisation/localisation.glade')  # creating object from XML(.glade files)


    def connect_handler(self, controller):
        self.handler = Handler(builder=self.__builder)
        self.handler.add_controller(controller)
        self.__builder.connect_signals(self.handler)
        
        
    def get_name(self):
        return self.name
