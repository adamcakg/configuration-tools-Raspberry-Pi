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
        return self.__builder.get_object('display')


    def destroy(self):
        del self
        
    def connect_builder(self):
        self.__builder = Gtk.Builder()                  # Initializing builder
        number_of_monitors = self.get_number_of_monitors()
        if number_of_monitors == 1:
            self.__builder.add_from_file('display/display_monitor.glade')
        elif number_of_monitors == 2:
            self.__builder.add_from_file('display/display_two_monitors.glade')

    def connect_handler(self, controller):
        self.handler = Handler(builder=self.__builder)
        self.handler.add_controller(controller)
        self.__builder.connect_signals(self.handler)
        
    def get_name(self):
        return self.name
    
    def get_number_of_monitors(self):
#        monitors = (os.popen("xrandr --listmonitors | grep Monitors: | cut -d ' ' -f 2").read())[:1]
 #       monitors = int(monitors)
  #      if monitors < 2:
   #         return 1
    #    elif monitors >1:
     #       return 2
        return 2