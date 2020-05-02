import os
from thread import Thread

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Handler:
    def __init__(self, builder, controller=None):
        self.builder = builder
        self.what_changed = []
        self.graphical_boot = True
        self.splash_screen_at_boot = False
        
        thread = Thread(self)
        
# ADDING CONTROLLER TO HANDLER
# ----------------------------------------------------------------------------------------------------------------------
    def add_controller(self, controller):
        self.controller = controller
        
# SETTING HOSTNAME
# ---------------------------------------------------------------
    def set_hostname(self):
        new_hostname = self.builder.get_object('hostname_entry').get_text()
        os.popen('sudo raspi-config nonint do_hostname {}'.format(new_hostname))
        
# GETTING HOSTNAME
# ---------------------------------------------------------------
    def get_hostname(self):
        hostname = os.popen("raspi-config nonint get_hostname").read()
        self.builder.get_object("hostname_entry").set_text(hostname)
        self.builder.get_object("hostname_entry").connect('changed', self.hostname_entry_changed)

# HOSTNAME ENTRY CHANGED
# ---------------------------------------------------------------   
    def hostname_entry_changed(self, widget):
        if 'hostname' not in self.what_changed:
            self.what_changed.append('hostname')
            self.set_apply_button('enable')
            
# GET AUTOLOGIN
# ---------------------------------------------------------------          
    def get_autologin(self):
        autologin = os.popen('raspi-config nonint get_autologin').read().rstrip()

        if autologin == '1':
            self.builder.get_object('autologin_switch').set_state(False)
            self.autologin = False
        elif autologin == '0':
            self.builder.get_object('autologin_switch').set_state(True)
            self.autologin = True
        self.builder.get_object("autologin_switch").connect('state-set', self.autologin_switch_changed)
        
# SET AUTOLOGIN
# ---------------------------------------------------------------  
    def set_autologin(self):
        boot_to_cli = os.popen('raspi-config nonint get_boot_cli').read().rstrip()
        state = self.builder.get_object('autologin_switch').get_state()
        
        if boot_to_cli == '0':
            if state:
                os.popen("sudo raspi-config nonint do_boot_behaviour B2")
            else:
                os.popen("sudo raspi-config nonint do_boot_behaviour B1")
        elif boot_to_cli == '1':
            if state:    
                os.popen("sudo raspi-config nonint do_boot_behaviour B4")
            else:
                os.popen("sudo raspi-config nonint do_boot_behaviour B3")
    
# AUTOLOGIN SWITCH CHANGES
# ---------------------------------------------------------------  
    def autologin_switch_changed(self, widget, state):
        if 'autologin' not in self.what_changed:
            self.what_changed.append('autologin')
            self.set_apply_button('enable')
# PASSWORD MODAL
# ---------------------------------------------------------------
    def compare(self, string1, string2):       # checking if strings are the same
        if string1 == '' or string2 == '':
            return False
        elif string1 == string2:
            return True
        else:
            return False
        
    def create_password_modal(self, widget):
        dialog = self.builder.get_object('password_modal')
        dialog.set_attached_to(self.builder.get_object('system'))
        dialog.show_all()
        

    def delete_password_modal(self, widget=None):
        dialog = self.builder.get_object('password_modal')
        self.builder.get_object('password_entry').set_text('')
        self.builder.get_object('confirmed_password_entry').set_text('')
        dialog.hide()
        
    def change_password(self, widget):
        password = self.builder.get_object('password_entry').get_text()
        confirmed = self.builder.get_object('confirmed_password_entry').get_text()
        
        if password == '':
            self.builder.get_object('not_match_password_label').set_opacity(0)
            self.builder.get_object('pasword_missing_label').set_opacity(1)
        elif self.compare(password, confirmed):  # checking if passwords are the same
            whoami = os.popen('whoami').read().rstrip()
            os.system('echo "{}:{}" | sudo chpasswd'.format(whoami, password))
        
            self.delete_password_modal()
        else:
            self.builder.get_object('pasword_missing_label').set_opacity(0)
            self.builder.get_object('not_match_password_label').set_opacity(1)
        
        
# BOOT TO DESKTOP
# ----------------------------------------------------------------
    def boot_to_desktop_switch_changed(self, widget, state):
        self.graphical_boot = state
        if 'boot_option' not in self.what_changed:
            self.what_changed.append('boot_option')
            self.set_apply_button('enable') 
                
            
# SETUP BOOT_TO_DESKTOP_SWITCH
# -----------------------------------------------------------------
    def get_boot_option(self):
        to_cli = os.popen('raspi-config nonint get_boot_cli').read().rstrip()
        if to_cli == '1':
            self.builder.get_object('boot_to_desktop_switch').set_state(True)
        elif to_cli == '0':
            self.builder.get_object('boot_to_desktop_switch').set_state(False)
        self.builder.get_object("boot_to_desktop_switch").connect('state-set', self.boot_to_desktop_switch_changed)
            
    def set_boot_option(self, state, autologin):
        if state == False:
            if autologin == False:
                os.popen('sudo raspi-config nonint do_boot_behaviour B1')
            else:
                os.popen('sudo raspi-config nonint do_boot_behaviour B2')
        elif state == True:
            if autologin == False:
                os.popen('sudo raspi-config nonint do_boot_behaviour B3')
            else:
                os.popen('sudo raspi-config nonint do_boot_behaviour B4')
        
# WAIT FOR NETWORK TO BOOT
# ------------------------------------------------------------------------
    def get_wait_for_network(self):
        wait = os.popen('raspi-config nonint get_boot_wait').read().rstrip()
        if wait == '1':
            self.builder.get_object('network_at_boot_switch').set_state(False)
        elif wait == '0':
            self.builder.get_object('network_at_boot_switch').set_state(True)
        self.builder.get_object("network_at_boot_switch").connect('state-set', self.network_at_boot_switch_changed)
            
    def network_at_boot_switch_changed(self, widget, state):
        if 'network_at_boot' not in self.what_changed:
            self.what_changed.append('network_at_boot')
            self.set_apply_button('enable') 

    def set_wait_for_network(self):
        wait = self.builder.get_object('network_at_boot_switch').get_state()
        if wait:
            os.popen('sudo raspi-config nonint do_boot_wait 0')
        else:
            os.popen("sudo raspi-config nonint do_boot_wait 1")
        
# SPLASH SCREEN
# --------------------------------------------------------------------------------
    def get_splash_screen(self):
        splash_screen = os.popen('raspi-config nonint get_boot_splash').read().rstrip()
        if splash_screen == '0':
            self.builder.get_object('splash_screen_switch').set_state(True)
            self.splash_screen_at_boot = True
        else:
            self.builder.get_object('splash_screen_switch').set_state(False)
        self.builder.get_object("splash_screen_switch").connect('state-set', self.splash_screen_switch_changed)
       
    def splash_screen_switch_changed(self, widget, state):
        self.splash_screen_at_boot = state
        if 'splash_screen' not in self.what_changed:
            self.what_changed.append('splash_screen')
            self.set_apply_button('enable')

    def set_splash_screen(self):
        os.popen('sudo raspi-config nonint do_boot_splash {}'.format(1-int(self.splash_screen_at_boot)))
        
# SET APPLY
# ---------------------------------------------------------------        
    def set_apply_button(self, action):
        if action == 'disable':
            self.builder.get_object("apply_button").set_sensitive(False)
        elif action == 'enable':
            if len(self.what_changed) < 2:
                self.builder.get_object("apply_button").set_sensitive(True)
            
# APPLY METHOD
# ---------------------------------------------------------------          
    def apply(self, widget):
        for item in self.what_changed:
            if item == 'hostname':
                self.set_hostname()
            elif item == 'autologin':
                self.set_autologin()
            elif item == 'boot_option':
                self.set_boot_option(self.graphical_boot, self.autologin)
            elif item == 'network_at_boot':
                self.set_wait_for_network()
            elif item == 'splash_screen':
                self.set_splash_screen()
        
        self.what_changed = []
        self.set_apply_button('disable')

# ---------------------------------------------------------------  
    def thread_function(self):
        self.set_apply_button('disable')
        self.get_hostname()
        self.get_autologin()
        self.get_boot_option()
        self.get_wait_for_network()
        self.get_splash_screen()
        
