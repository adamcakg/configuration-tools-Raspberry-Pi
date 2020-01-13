import wifipage as wifi_page
import settings as settings
from .handler import Handler
from keeper import keeper
from thread import Thread

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class PasswordPage:

    def __init__(self):
        self.__builder = Gtk.Builder()                                                  # creating builder
        self.__builder.add_from_file('passwordpage/password_page.glade')                # adding XML file

        if 'passwordpage' in keeper:                                    # checking if password is already in keeper
            self.__builder.get_object('password').set_text(keeper['passwordpage']['password'])
            self.__builder.get_object('confirmed').set_text(keeper['passwordpage']['password'])
        else:
            self.default()
            
        self.handler = Handler(builder=self.__builder)

# METHOD TO GO NEXT
# ----------------------------------------------------------------------------------------------------------------------
    def next(self, controller):                                         # next page
        controller.set_state(wifi_page.WifiPage())

# METHOD TO GO BACK
# ----------------------------------------------------------------------------------------------------------------------
    def back(self, controller):                                         # previous page
        controller.set_state(settings.SettingsPage())

# METHOD TO GET XML OBJECT
# ----------------------------------------------------------------------------------------------------------------------
    def get_xml_object(self):
        return self.__builder.get_object('password_page')

# METHOD TO DESTROY ITSELF
# ----------------------------------------------------------------------------------------------------------------------
    def destroy(self):                                                  # destroying object
        del self

# METHOD TO CONNECT HANDLER
# ----------------------------------------------------------------------------------------------------------------------
    def connect_handler(self, controller):                              # connecting handler to page
        self.handler.add_controller(controller)
        self.__builder.connect_signals(self.handler)

# METHOD TO SET DEFAULTS
# ----------------------------------------------------------------------------------------------------------------------
    def default(self):                                                  # setting default settings on page
        dict_to_add = {
            'passwordpage': {'password': ''}
        }
        keeper.update(dict_to_add)

# METHOD EXECUTE PAGE
# ----------------------------------------------------------------------------------------------------------------------
    def execute(self):                                                  # executing page content
        thread = Thread(self.handler)
        self.handler.create_modal()
        
        while(thread.alive()):
             while Gtk.events_pending():
                Gtk.main_iteration_do(True)
        self.handler.delete_modal()
        
        

