import gi
from .handler import Handler

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Main:
    def __init__(self):
        self.__builder = Gtk.Builder()                  # Initializing builder
        self.__builder.add_from_file('main/main.glade')   # creating object from XML(.glade files)
        
        self.handler = Handler(builder=self.__builder)
        
    
    def next(self, controller):
        # there will be page where i was 
        pass
    
    def get_xml_object(self):
        return self.__builder.get_object('main')

    def destroy(self):
        del self

    def connect_handler(self, controller):
        self.handler.add_controller(controller)
        self.__builder.connect_signals(self.handler)
        
        
