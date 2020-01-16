import wifipage as wifi_page
import softwarepage as softwarepage
from .handler import Handler
from thread import Thread


import gi
import requests

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class UpdatePage:
    def __init__(self):
        self.__builder = Gtk.Builder()                  # Initializing builder
        self.__builder.add_from_file('update_page/update_page.glade')   # creating object from XML(.glade files)
        self.handler = Handler(builder=self.__builder)

    def next(self, controller):
        controller.set_state(softwarepage.SoftwarePage())

    def back(self, controller):
        controller.set_state(wifi_page.WifiPage())

    def get_xml_object(self):
        return self.__builder.get_object('update_page')

    def destroy(self):
        del self

    def connect_handler(self, controller):
        self.handler.add_controller(controller)
        self.__builder.connect_signals(self.handler)
        
    def execute(self):
        try:
            request = requests.get('http://www.raspberrypi.com/', timeout=30)
        except requests.ConnectionError:
            self.__builder.get_object('no_internet_label').set_opacity(1)
            return
        
        thread = Thread(self.handler)
        self.handler.create_modal()
        
        while(thread.alive()):
             while Gtk.events_pending():
                Gtk.main_iteration_do(True)
        self.handler.delete_modal()
        
        
        
        
        
