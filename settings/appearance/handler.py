from thread import Thread
import os

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,GLib


class Handler:
    def __init__(self, builder, controller=None):
        self.builder = builder
        self.changed = False
        self.monitors = 1
        
        
        Thread(self)
        
        
        
        #self.set_apply_button('disable')
# ADDING CONTROLLER TO HANDLER
# ---------------------------------------------------------------------------------
    def add_controller(self, controller):
        self.controller = controller

# RELOADING SETTINGS
# -----------------------------------------------------------------------------------
    def reload_lxpanel(self):
        os.popen("lxpanelctl refresh")

    def reload_openbox(self):
        os.popen("openbox --reconfigure")

    def reload_pcmanfm(self):
        os.popen("pcmanfm --reconfigure")

    def reload_lxsession(self):
        os.popen("lxsession -r")

# ---------------------------------------------------------------------------------------
    def check_dir(path):
        GLib.mkdir_with_parents(path, 6)
        
# ---------------------------------------------------------------------------------------
        
    def get_openbox_file(self):
        filename = GLib.getenv ("DESKTOP_SESSION").lower() + '-rc.xml'
        path = GLib.get_user_config_dir() + '/openbox/' + filename
        return path
    
    def get_lxsession_file(self):
        desktop_session = GLib.getenv ("DESKTOP_SESSION")
        path = GLib.get_user_config_dir() + '/lxsession/' + desktop_session + "/desktop.conf"
        return path
    
    def get_lxpanel_file(self):
        desktop_session = GLib.getenv ("DESKTOP_SESSION")
        path = GLib.get_user_config_dir() + '/lxpanel/' + desktop_session + "/panels/panel"
        return path

    def get_pcmanfm_file(self, desktop):
        desktop_session = GLib.getenv ("DESKTOP_SESSION")
        path = GLib.get_user_config_dir() + "/pcmanfm/" + desktop_session + ''.format("desktop-items-0.conf" if desktop else "desktop-items-1.conf")
        
        return path
    
    def get_pcmanfm_g_file(self):
        desktop_session = GLib.getenv ("DESKTOP_SESSION")
        path = GLib.get_user_config_dir() + "/pcmanfm/" + desktop_session + "/pcmanfm.conf"
        return path
        
    def get_libfm_file(self):
        desktop_session = GLib.getenv ("DESKTOP_SESSION")
        path = GLib.get_user_config_dir() + "/libfm/libfm.conf"
        return path
# NUMBER OF MONITORS
# ---------------------------------------------------------------------------------
    def get_number_of_monitors(self):
        self.monitors = (os.popen("xrandr --listmonitors | grep Monitors: | cut -d ' ' -f 2").read())[:1]
        self.monitors = int(self.monitors)
        
        if self.monitors < 0:
            self.monitors = 1
        elif self.monitors >2:
            self.monitors = 2
    
# GET SETTINGS
# ---------------------------------------------------------------------------------   
    def get_settings(self):
        #desktop_session = GLib.getenv ("DESKTOP_SESSION")
        #print(GLib.get_user_config_dir())
        #GLib.mkdir_with_parents(path, 6)
        pass
    
    
    
# SET APPLY
# ---------------------------------------------------------------        
    def set_apply_button(self, action):
        if action == 'disable':
            self.builder.get_object("apply_button").set_sensitive(False)
        elif action == 'enable':
            if self.changed:
                self.builder.get_object("apply_button").set_sensitive(True)
                
# APPLY METHOD
# ---------------------------------------------------------------          
    def apply(self, widget):
        
        
        
        self.set_apply_button('disable')
        
        
    
    def thread_function(self):
        self.get_number_of_monitors()
        self.get_settings()
    
       
        print(self.get_pcmanfm_file(0))
        print(self.get_openbox_file())
        print(self.get_lxsession_file())
        print(self.get_lxpanel_file())
        print(self.get_pcmanfm_g_file())
        print(self.get_libfm_file())
        
    