from thread import Thread
from .locale import get_language_and_country
from .locale import languages

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Handler:
    def __init__(self, builder, controller=None):
        self.builder = builder
        
        thread = Thread(self)
        
        while thread.alive() :
             while Gtk.events_pending():
                Gtk.main_iteration_do(True)

    # ADDING CONTROLLER TO HANDLER
    # ----------------------------------------------------------------------------------------------------------------------
    def add_controller(self, controller):
        self.controller = controller
    
    
    def create_localisation_modal(self, widget):
        dialog = self.builder.get_object('localisation_modal')
        dialog.set_attached_to(self.builder.get_object('localisation'))
        dialog.show_all()
        

    def delete_localisation_modal(self, widget=None):
        dialog = self.builder.get_object('localisation_modal')
        dialog.hide()
    
    
    def change_option_in_localisation(self, widget):
        pass
    
    
    
    
        
    def thread_function(self):
        get_language_and_country()