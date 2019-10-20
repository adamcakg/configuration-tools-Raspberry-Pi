import test.update_page as update_page
import test.settings as settings
from .handler import Handler
from test.keeper import is_in_keeper
from test.keeper import keeper
from test.keeper import add_to_keeper

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class PasswordPage:

    def __init__(self):
        self.__builder = Gtk.Builder()
        self.__builder.add_from_file('passwordpage/password_page.glade')
        # TODO --------
        if is_in_keeper('passwordpage'):
            self.__builder.get_object('password').set_text(keeper['passwordpage']['password'])
            self.__builder.get_object('confirmed_password').set_text(keeper['passwordpage']['password'])

        else:
            self.default()

        # TODO --------

    def next(self, controller):
        controller.set_state(update_page.UpdatePage())

    def back(self, controller):
        controller.set_state(settings.SettingsPage())

    def get_xml_object(self):
        return self.__builder.get_object('password_page')

    def destroy(self):
        del self

    def connect_handler(self, controller):
        self.__builder.connect_signals(Handler(controller))

    def default(self):
        dict_to_add = {
            'passwordpage': {'password': ''}
        }
        add_to_keeper(dict_to_add)
