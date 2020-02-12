import os
from thread import Thread
from .boot_option import set_boot_option
from . boot_option import get_boot_wait

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Handler:
    def __init__(self, builder, controller=None):
        self.builder = builder
        self.what_changed = []
        self.hostname = ''
        self.autologin = False
        self.graphical_boot = True
        self.network_at_boot = False
        
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
        new_hostname = self.builder.get_object('hostname_entry').get_text()
        with open('/etc/hostname', 'w') as file:
            file.write(new_hostname + '\n')
            
        hosts = os.popen('cat /etc/hosts').read()
        hosts = hosts.replace(self.hostname, new_hostname)
        
        with open('/etc/hosts', 'w') as file:
            file.write(hosts)
        
        self.hostname = new_hostname
        
            
# GETTING HOSTNAME
# ---------------------------------------------------------------
    def get_hostname(self):
        self.hostname = os.popen("cat /etc/hostname").read()[:-1]
        self.builder.get_object("hostname_entry").set_text(self.hostname)

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
            print('#autologin-user=pi')
            self.builder.get_object('autologin_switch').set_state(False)
            self.autologin = False
        elif 'autologin-user=pi' in lightdm:
            self.builder.get_object('autologin_switch').set_state(True)
            self.autologin = True
        

# SET AUTOLOGIN
# ---------------------------------------------------------------  
    def set_autologin(self):
        lightdm = os.popen('cat /etc/lightdm/lightdm.conf').read()
        if self.builder.get_object('autologin_switch').get_state() == True:
            if '#autologin-user=pi' in lightdm:
                lightdm = lightdm.replace('#autologin-user=pi', 'autologin-user=pi')
            if '#autologin-user=' in lightdm:
                lightdm = lightdm.replace('#autologin-user=', 'autologin-user=pi')
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
            os.system('echo "{}" | passwd'.format(password + '\n' + password))
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
        boot_option = os.popen('systemctl get-default').read()
        if boot_option == 'graphical.target':
            self.builder.get_object('boot_to_desktop_switch').set_state(True)
        elif boot_option == 'multi-user.target':
            self.builder.get_object('boot_to_desktop_switch').set_state(False)
            
            
# WAIT FOR NETWORK TO BOOT
# ------------------------------------------------------------------------
    def get_wait_for_network(self):
        wait = get_boot_wait() 
        if wait == 0:
            self.builder.get_object('network_at_boot_switch').set_state(False)
        elif wait == 1:
            self.builder.get_object('network_at_boot_switch').set_state(True)
            
    def network_at_boot_switch_changed(self, widget, state):
        self.network_at_boot = state
        if 'network_at_boot' not in self.what_changed:
            self.what_changed.append('network_at_boot')
            self.set_apply_button('enable') 

    def set_wait_for_network(self):
        if self.network_at_boot == True:
            os.popen('mkdir -p /etc/systemd/system/dhcpcd.service.d/')
            os.popen('''cat > /etc/systemd/system/dhcpcd.service.d/wait.conf << EOF
[Service]
ExecStart=
ExecStart=/usr/lib/dhcpcd5/dhcpcd -q -w
EOF''')
        elif self.network_at_boot == False:
            os.popen('rm -f /etc/systemd/system/dhcpcd.service.d/wait.conf')
       
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
                set_boot_option(self.graphical_boot, self.autologin)
            elif item == 'network_at_boot':
                self.set_wait_for_network()
        
          
        self.what_changed = []
        self.set_apply_button('disable')


# ---------------------------------------------------------------  
    def thread_function(self):
        self.get_hostname()
        self.get_autologin()
        self.get_boot_option()
        self.get_wait_for_network()
        
