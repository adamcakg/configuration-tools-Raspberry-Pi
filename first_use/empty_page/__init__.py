import softwarepage as softwarepage
from .handler import Handler
from page import Page

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf


class EmptyPage(Page):

    def __init__(self):
        self.__builder = Gtk.Builder()                  # Initializing builder
        self.__builder.add_from_file('/opt/first_use/empty_page/empty_page.glade')  
        
    def next(self, controller):
        controller.set_state() # Here add next page f.e. softwarepage.SoftwarePage()

    def back(self, controller):
        controller.set_state() # Here add previous page f.e. softwarepage.SoftwarePage()

    def get_xml_object(self):
        return self.__builder.get_object('empty_page')

    def destroy(self):
        del self

    def connect_handler(self, controller):
        self.__builder.connect_signals(Handler(controller))
