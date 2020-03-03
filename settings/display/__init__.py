import os

import gi
from .handler import Handler
from page import Page


gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Display(Page):
    def __init__(self):
        self.name = "Display"
        self.__builder = None
        self.handler = None
        self.header = None
        
        
    def get_xml_object(self):
        number_of_monitors = self.get_number_of_monitors()
        if number_of_monitors == 1:
            return self.__builder.get_object('one_display')
        elif number_of_monitors == 2:
            return self.__builder.get_object('two_displays')

    def destroy(self):
        del self
        
    def connect_builder(self):
        self.__builder = Gtk.Builder()                  # Initializing builder
        self.__builder.add_from_file('display/display.glade')   # creating object from XML(.glade files)
      

    def connect_handler(self, controller):
        self.handler = Handler(builder=self.__builder)
        self.handler.add_controller(controller)
        self.__builder.connect_signals(self.handler)

    def connect_header(self, header):
        self.header = header
        self.header.set_title(self.name)
        
    def get_name(self):
        return self.name
    
    def get_number_of_monitors(self):
        monitors = (os.popen("xrandr --listmonitors | grep Monitors: | cut -d ' ' -f 2").read())[:1]
        monitors = int(monitors)
        print(monitors)
        if monitors < 2:
            return 1
        elif monitors >1:
            return 2
        