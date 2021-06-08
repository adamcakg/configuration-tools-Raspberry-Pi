import update_page as update_page
import passwordpage as password_page
from .handler import Handler
from page import Page

from thread import Thread

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class WifiPage(Page):
    def __init__(self):
        self.__builder = Gtk.Builder()                  # Initializing builder
        self.__builder.add_from_file('/opt/first_use/wifipage/wifi.glade')   # creating object from XML(.glade files)
        self.handler = Handler(builder=self.__builder)
        
        self.execute()

# METHOD TO GO NEXT
# ----------------------------------------------------------------------------------------------------------------------
    def next(self, controller):
        controller.set_state(update_page.UpdatePage())

# METHOD TO GO BACK
# ----------------------------------------------------------------------------------------------------------------------
    def back(self, controller):
        controller.set_state(password_page.PasswordPage())

# METHOD TO GET XML OBJECT
# ----------------------------------------------------------------------------------------------------------------------
    def get_xml_object(self):
        return self.__builder.get_object('wifi')

# METHOD TO DESTROY ITSELF
# ----------------------------------------------------------------------------------------------------------------------
    def destroy(self):
        del self

# METHOD TO CONNECT HANDLER
# ----------------------------------------------------------------------------------------------------------------------
    def connect_handler(self, controller):
        self.handler.add_controller(controller)
        self.__builder.connect_signals(self.handler)

# METHOD TO EXECUTE PAGE
# ----------------------------------------------------------------------------------------------------------------------
    def execute(self):
        Thread(self.handler)
        
    

        
