import update_page as update_page
import settings as settings
from .handler import Handler
from keeper import keeper

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

# METHOD TO GO NEXT
# ----------------------------------------------------------------------------------------------------------------------
    def next(self, controller):                                         # next page
        controller.set_state(update_page.UpdatePage())

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
        self.__builder.connect_signals(Handler(controller, self.__builder))

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
        print('Password page executed')

        # import os
        # password = keeper['passwordpage']['password'] + '\n' + keeper['passwordpage']['password']
        # os.system('echo "{}" | sudo passwd "pi"'.format(password))

