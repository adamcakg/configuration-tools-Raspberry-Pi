import os
from thread import Thread

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Handler:
    def __init__(self, builder, controller=None):
        self.builder = builder
        self.what_changed = []
        
        thread = Thread(self)
        
        while thread.alive() :
             while Gtk.events_pending():
                Gtk.main_iteration_do(True)
                
                
        self.set_apply_button('disable')

# ADDING CONTROLLER TO HANDLER
# ----------------------------------------------------------------------------------------------------------------------
    def add_controller(self, controller):
        self.controller = controller
        
# SETTING HOSTNAME
# ---------------------------------------------------------------
    def set_hostname(self):
        with open('/etc/hostname', 'w') as file:
            file.write(self.builder.get_object('hostname_entry').get_text() + '\n')
            
# GETTING HOSTNAME
# ---------------------------------------------------------------
    def get_hostname(self):
        hostname = os.popen("cat /etc/hostname").read()
        self.builder.get_object("hostname_entry").set_text(hostname[:-1])

# HOSTNAME ENTRY CHANGED
# ---------------------------------------------------------------   
    def hostname_entry_changed(self, widget):
        if 'hostname' not in self.what_changed:
            self.what_changed.append('hostname')
            self.set_apply_button('enable')
            
# GET AUTOLOGIN
# ---------------------------------------------------------------          
    def get_autologin(self):
        lightdm = os.popen('cat /etc/lightdm/lightdm.conf').read()
        if '#autologin-user=pi' in lightdm:
            self.builder.get_object('autologin_switch').set_state(False)
        else:
            self.builder.get_object('autologin_switch').set_state(True)

# SET AUTOLOGIN
# ---------------------------------------------------------------  
    def set_autologin(self):
        lightdm = os.popen('cat /etc/lightdm/lightdm.conf').read()
        if self.builder.get_object('autologin_switch').get_state() == True:
            if '#autologin-user=pi' in lightdm:
                lightdm = lightdm.replace('#autologin-user=pi', 'autologin-user=pi')
        else:
            if 'autologin-user=pi' in lightdm:
                lightdm = lightdm.replace('autologin-user=pi', '#autologin-user=pi')
        
        with open('/etc/lightdm/lightdm.conf', 'w') as file:
            file.write(lightdm)
        
# AUTOLOGIN SWITCH CHANGES
# ---------------------------------------------------------------  
    def autologin_switch_changed(self, widget, state):
        if 'autologin' not in self.what_changed:
            self.what_changed.append('autologin')
            self.set_apply_button('enable')
# PASSWORD MODAL
# ---------------------------------------------------------------  
    def create_password_modal(self, widget):
        dialog = self.builder.get_object('password_modal')
        dialog.set_attached_to(self.builder.get_object('system'))
        dialog.show_all()
        

    def delete_password_modal(self, widget=None):
        dialog = self.builder.get_object('password_modal')
        dialog.hide()
           
           
# SET APPLY
# ---------------------------------------------------------------        
    def set_apply_button(self, action):
        if action == 'disable':
            self.builder.get_object("apply_button").set_sensitive(False)
        elif action == 'enable':
            self.builder.get_object("apply_button").set_sensitive(True)
            
            
# APPLY METHOD
# ---------------------------------------------------------------          
    def apply(self, widget):
        for item in self.what_changed:
            if item == 'hostname':
                self.set_hostname()
            elif item == 'autologin':
                self.set_autologin()
          
        self.what_changed = []
        self.set_apply_button('disable')


# ---------------------------------------------------------------  
    def thread_function(self):
        self.get_hostname()
        self.get_autologin()
        
