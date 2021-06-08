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
        return self.builder.get_object('wifi')

    def destroy(self):
        del self
        
    def connect_builder(self):
        self.builder = Gtk.Builder()                  # Initializing builder
        self.builder.add_from_file('/opt/settings/wifi/wifi.glade')  

    def connect_handler(self, controller):
        self.handler = Handler(builder=self.builder)
        self.handler.add_controller(controller)
        self.builder.connect_signals(self.handler)
        
    def get_name(self):
        return self.name

    def get_icon(self):
        return '/opt/settings/wifi/img/wifi.svg'
    
