import test.update_page as update_page
import test.settings as settings
from .handler import Handler
from test.keeper import keeper

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class PasswordPage:

    def __init__(self):
        self.__builder = Gtk.Builder()                                                  # creating builder
        self.__builder.add_from_file('passwordpage/password_page.glade')                # adding XML file

        if 'passwordpage' in keeper:                                    # checking if password is already in keeper
            self.__builder.get_object('password').set_text(keeper['passwordpage']['password'])
            self.__builder.get_object('confirmed_password').set_text(keeper['passwordpage']['password'])
        else:
            self.default()



    @staticmethod
    def next(controller):                                         # next page
        controller.set_state(update_page.UpdatePage())

    @staticmethod
    def back(controller):                                         # previous page
        controller.set_state(settings.SettingsPage())

    def get_xml_object(self):
        return self.__builder.get_object('password_page')

    def destroy(self):                                                  # destroying object
        del self

    def connect_handler(self, controller):                              # connecting handler to page
        self.__builder.connect_signals(Handler(controller))

    @staticmethod
    def default():                                                  # setting default settings on page
        dict_to_add = {
            'passwordpage': {'password': ''}
        }
        keeper.update(dict_to_add)

    def execute(self):                                                  # executing page content
        print('Password page executed')

        # import os
        # mycmd = os.popen('pip install --upgrade pip').read()
        # print(mycmd)


