import gi
from .handler import Handler
from page import Page
from thread import Thread

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Wifi(Page):
    def __init__(self):
        self.name = "Wifi"
        self.buidler = None
        self.handler = None
        self.header = None
        
    def get_xml_object(self):
        return self.__builder.get_object('wifi')

    def destroy(self):
        del self
        
    def connect_builder(self):
        self.__builder = Gtk.Builder()                  # Initializing builder
        self.__builder.add_from_file('wifi/wifi.glade')   # creating object from XML(.glade files)

    def connect_handler(self, controller):
        self.handler = Handler(builder=self.__builder)
        self.handler.add_controller(controller)
        self.__builder.connect_signals(self.handler)
        
    def get_name(self):
        return self.name
    
# METHOD TO EXECUTE PAGE
# ----------------------------------------------------------------------------------------------------------------------
    def execute(self):
        Thread(self.handler)
        
        
        
        