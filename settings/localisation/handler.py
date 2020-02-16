from thread import Thread
from .locale import get_language_and_country

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Handler:
    def __init__(self, builder, controller=None):
        self.builder = builder
        self.option = None
        self.language_store = None
        self.country = []
        
        thread = Thread(self)
        
      

    # ADDING CONTROLLER TO HANDLER
    # ----------------------------------------------------------------------------------------------------------------------
    def add_controller(self, controller):
        self.controller = controller
    
    
    def create_localisation_modal(self, widget):
        self.create_locale_modal()
        
        dialog = self.builder.get_object('localisation_modal')
        dialog.set_attached_to(self.builder.get_object('localisation'))
        dialog.show_all()
    
    def create_locale_modal(self):
        self.builder.get_object('localisation_dialog_label').set_text('Choose a locale:')
        combo_box = self.builder.get_object('localisation_combo_box')
        combo_box.set_model(self.language_store)

    
    def create_timezone_modal(self):
        pass
    
    def create_keyboard_modal(self):
        pass
    
    def create_country_modal(self):
        pass

    def delete_localisation_modal(self, widget=None):
        dialog = self.builder.get_object('localisation_modal')
        dialog.hide()
    
    
    def change_option_in_localisation(self, widget):
        pass
    
    
    
    
        
    def thread_function(self):
        languages, self.country = get_language_and_country()
        self.language_store = Gtk.ListStore(str)
        for language in languages:
            self.language_store.append([language])
        
        
        