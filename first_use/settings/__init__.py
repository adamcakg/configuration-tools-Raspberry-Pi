import passwordpage as passwordpage
import welcome as welcome
from .handler import Handler

import threading

from keeper import keeper

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class SettingsPage:

    def __init__(self):
        self.__builder = Gtk.Builder()                            # Initializing builder
        self.__builder.add_from_file('settings/settings.glade')   # creating object from XML(.glade files)
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
        print('locales execute')
        #t3 = threading.Thread(target=self.__builder.get_object('window').show())
        #self.__builder.get_object('window').show()
        #self.handler.modal()
        
  #      t1 = threading.Thread(target=self.handler.set_timezone())
   #     t2 = threading.Thread(target=self.handler.set_locale())
        
    #    t1.start()
     #   t2.start()
        
        self.handler.set_timezone()
        self.handler.set_locale()
        
        

