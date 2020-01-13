import gi
from .handler import Handler

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Interfaces:
    def __init__(self):
        self.__builder = Gtk.Builder()                  # Initializing builder
        self.__builder.add_from_file('interfaces/interfaces.glade')   # creating object from XML(.glade files)
        
        self.handler = Handler(builder=self.__builder)
        self.header = None
        
    def get_xml_object(self):
        return self.__builder.get_object('interfaces')

    def destroy(self):
        del self

    def connect_handler(self, controller):
        self.handler.add_controller(controller)
        self.__builder.connect_signals(self.handler)

    def connect_header(self, header):
        self.header = header
        self.header.set_title('Interfaces')
        self.header.enable_button('left')
        self.header.disable_button('right')
        