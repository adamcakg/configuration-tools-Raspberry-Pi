import passwordpage as passwordpage
import welcome as welcome
from .handler import Handler
from thread import Thread
from keeper import keeper
from page import Page

import locale
from locale import gettext as _

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class SettingsPage(Page):

    def __init__(self):
        self.__builder = Gtk.Builder()                            # Initializing builder
        self.__builder.add_from_file('/opt/first_use/settings/settings.glade')   # creating object from XML(.glade files)
        self.handler = Handler(builder=self.__builder)
        
        if 'settingspage' not in keeper:
            self.default()

        self.handler.insert_countries()
        self.handler.insert_languages()
        self.handler.insert_timezones()
        
# METHOD TO GO NEXT
# ----------------------------------------------------------------------------------------------------------------------
    def next(self, controller): 
        controller.set_state(passwordpage.PasswordPage())

# METHOD TO GO BACK
# ----------------------------------------------------------------------------------------------------------------------
    def back(self, controller):
        controller.set_state(welcome.WelcomePage())

# METHOD TO GET XML OBJECT
# ----------------------------------------------------------------------------------------------------------------------
    def get_xml_object(self):
        return self.__builder.get_object('settings')

# METHOD TO DESTROY ITSELF
# ----------------------------------------------------------------------------------------------------------------------
    def destroy(self):
        del self

# METHOD TO CONNECT HANDLER
# ----------------------------------------------------------------------------------------------------------------------
    def connect_handler(self, controller):
        self.handler.add_controller(controller)
        self.__builder.connect_signals(self.handler)

# METHOD TO SET DEFAULT
# ----------------------------------------------------------------------------------------------------------------------
    def default(self):
        dict_to_add = {'settingspage': {'country': 'United States','language': 'American English',
                                        'timezone': 'New York'}}
        keeper.update(dict_to_add)

# METHOD TO EXECUTE PAGE
# ----------------------------------------------------------------------------------------------------------------------
    def execute(self):   
        thread = Thread(self.handler)
        self.handler.create_modal()
        
        while(thread.alive()):
             while Gtk.events_pending():
                Gtk.main_iteration_do(True)
        self.handler.delete_modal()


    def apply_locale(self , current_lang ):
        domain = "firstuse"
        local_path = domain +"/data/locale"  # fixme pathlib
        locale.bindtextdomain(domain , local_path )
        locale.textdomain(domain)
        locale.setlocale(locale.LC_ALL, 'ar_AE.utf8')
        # note that language is "ar_AE.utf8" not "ar" or "ar_AE"
        self.builder.set_translation_domain(domain )


