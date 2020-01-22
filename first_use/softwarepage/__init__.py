import update_page as update_page
import allset as allset
from .handler import Handler
from thread import Thread

from page import Page

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class SoftwarePage(Page):
    def __init__(self):
        self.__builder = Gtk.Builder()                  # Initializing builder
        self.__builder.add_from_file('softwarepage/software_page.glade')   # creating object from XML(.glade files)
        self.handler = Handler(builder=self.__builder)

    def next(self, controller):
        controller.set_state(allset.AllSet())

    def back(self, controller):
        controller.set_state(update_page.UpdatePage())

    def get_xml_object(self):
        return self.__builder.get_object('software_page')

    def destroy(self):
        del self

    def connect_handler(self, controller):
        self.handler.add_controller(controller)
        self.__builder.connect_signals(self.handler)

    def execute(self):
        thread = Thread(self.handler)
        
        self.handler.create_modal()
        
        while(thread.alive()):
             while Gtk.events_pending():
                Gtk.main_iteration_do(True)
        self.handler.delete_modal()
        
        
        
        
        
        
        