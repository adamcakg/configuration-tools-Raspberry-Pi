import gi
from .handler import Handler

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Main:
    def __init__(self, next_page = None):
        self.__builder = Gtk.Builder()                  # Initializing builder
        self.__builder.add_from_file('main/main.glade')   # creating object from XML(.glade files)
        
        self.handler = Handler(builder=self.__builder)
        self.header = None
        
        self.next_page = next_page

    def next(self, controller):
        if self.next_page:
            controller.set_state(self.next_page)

    
    def get_xml_object(self):
        return self.__builder.get_object('main')

    def destroy(self):
        del self

    def connect_handler(self, controller):
        self.handler.add_controller(controller)
        self.__builder.connect_signals(self.handler)

    def connect_header(self, header):
        self.header = header
        self.header.set_title('Settings')
        self.header.disable_button('left')
        if self.next_page:
            self.header.enable_button('right')
        else:
            self.header.disable_button('right')
        
        
