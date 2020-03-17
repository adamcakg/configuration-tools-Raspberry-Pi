import gi
from .handler import Handler
from page import Page

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class EmptyPage(Page):
    def __init__(self):
        """
            Here define name of page as well as builder and handler of page

        """
        self.name = "EmptyPage"  
        self.__builder = None
        self.handler = None
        
    def get_xml_object(self):
        """
            Here return main object from .glade file (page to display)

        """
        return self.__builder.get_object('empty_page')

    def destroy(self):
        """
            Method for destroy the page
            
        """
        del self
        
    def connect_builder(self):
        """
            Here creating builder for page as well as adding .glade file into it
            [folder]/[name_of_glade_file]
            
        """
        self.__builder = Gtk.Builder()                  # Initializing builder
        self.__builder.add_from_file('empty_page/empty_page.glade')   # creating object from XML(.glade files)
      

    def connect_handler(self, controller):
        """
            Creating handler for page, adding controller to page and connecting signals with builder
            
        """
        self.handler = Handler(builder=self.__builder)
        self.handler.add_controller(controller)
        self.__builder.connect_signals(self.handler)
        
    def get_name(self):
        """
            Return name of page to display in navigation menu
        
        """
        return self.name
        