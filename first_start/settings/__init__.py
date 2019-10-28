
import test.passwordpage as passwordpage
import test.welcome as welcome
from .handler import Handler

from test.keeper import keeper


import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

language = ['English', 'Deutch', 'Slovak', 'Czech']
countries = ['England', 'Germany', 'Slovakia', 'Czech Republic']


class SettingsPage:

    def __init__(self):
        self.__builder = Gtk.Builder()                  # Initializing builder
        self.__builder.add_from_file('settings/settings.glade')   # creating object from XML(.glade files)
        self.insert_countries()

        if 'settingspage' in keeper:
            self.__builder.get_object('combo_box_country').set_active_id(keeper['settingspage']['country'])
            self.__builder.get_object('combo_box_language').set_active_id(keeper['settingspage']['language'])

        else:
            self.default()

    def next(self, controller):
        controller.set_state(passwordpage.PasswordPage())

    def back(self, controller):
        controller.set_state(welcome.WelcomePage())

    def get_xml_object(self):
        return self.__builder.get_object('settings')

    def destroy(self):
        del self

    def connect_handler(self, controller):
        self.__builder.connect_signals(Handler(controller))

    def insert_countries(self):
        countries_object = self.__builder.get_object('combo_box_country')
        language_object = self.__builder.get_object('combo_box_language')

        for index in range(len(countries)):
            countries_object.append(countries[index], countries[index])
            language_object.append(language[index], language[index])

    def default(self):
        dict_to_add = {
            'settingspage': {'country': 'England',
                             'language': 'English',
                             }
        }
        self.__builder.get_object('combo_box_country').set_active_id('England')
        self.__builder.get_object('combo_box_language').set_active_id('English')

        keeper.update(dict_to_add)

    def execute(self):
        pass
