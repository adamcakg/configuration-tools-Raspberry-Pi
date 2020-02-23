from thread import Thread
import os

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, Gdk


class Handler:
    def __init__(self, builder, controller=None):
        self.builder = builder
        self.changed = False
        self.monitors = 1
        self.pcman_file_desktop_0 = ''
        self.pcman_file_desktop_1 = ''
        self.mode_0 = ''
        self.mode_1 = ''
        self.wallpaper_path_0 = ''
        self.wallpaper_path_1 = ''
        self.bg_color_0 = ''
        self.bg_color_1 = ''
        self.fg_color_0 = ''
        self.fg_color_1 = ''
        
        
        Thread(self)
        
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
   
# GET PCMANFM FILE
# ---------------------------------------------------------------------------------------
    def get_pcmanfm_file(self, desktop, global_settings):
        desktop_session = GLib.getenv ("DESKTOP_SESSION")
        path = ( "/etc/xdg" if global_settings else GLib.get_user_config_dir()) + "/pcmanfm/" + desktop_session + '/{}'.format("desktop-items-0.conf" if desktop == 0 else "desktop-items-1.conf")
        return path
    
    def save_pcman_file(self, desktop):
        if desktop == 0:
            os.popen('sudo echo "{}" > {}'.format(self.pcman_file_desktop_0.rstrip(), self.get_pcmanfm_file(desktop, False)))
        else:
            os.popen('sudo echo "{}" > {}'.format(self.pcman_file_desktop_1.rstrip(), self.get_pcmanfm_file(desktop, False)))
        self.reload_pcmanfm()
# ---------------------------------------------------------------------------------------             
    
    def set_wallpaper_mode(self, desktop):
        if desktop == 0:
            self.mode_0 = self.pcman_file_desktop_0.split('\n')[1].split('=')
            self.builder.get_object('wallpaper_laytout_combo_box_1').set_active_id(self.mode_0[1]) # mode from pcmanfm file
        elif desktop == 1:
            self.mode_1 = self.pcman_file_desktop_1.split('\n')[1].split('=')
            self.builder.get_object('wallpaper_laytout_combo_box_2').set_active_id(self.mode_1[1]) # mode from pcmanfm file
    
    def wallpaper_mode_1_changed(self, widget):
        mode = widget.get_active_id()
        self.pcman_file_desktop_0 = self.pcman_file_desktop_0.replace(self.mode_0[1], mode)
        self.mode_0[1] = mode
        self.save_pcman_file(0)
        
        
    def wallpaper_mode_2_changed(self, widget):
        mode = widget.get_active_id()
        self.pcman_file_desktop_1 = self.pcman_file_desktop_1.replace(self.mode_1[1], mode)
        self.mode_1[1] = mode
        self.save_pcman_file(1)
# ---------------------------------------------------------------------------------------             
    def set_image_choosing_dialog(self, desktop):
        if desktop == 0:
            self.wallpaper_path_0 = self.pcman_file_desktop_0.split('\n')[3].split('=')[1]
            self.builder.get_object('image_choosing_dialog_0').set_filename(self.wallpaper_path_0)
        elif desktop == 1:
            self.wallpaper_path_1 = self.pcman_file_desktop_1.split('\n')[3].split('=')[1]
            self.builder.get_object('image_choosing_dialog_1').set_filename(self.wallpaper_path_1)
    
    def wallpaper_1_changed(self, widget):
        new_file_path = widget.get_filename()
        self.pcman_file_desktop_0 = self.pcman_file_desktop_0.replace(self.wallpaper_path_0, new_file_path)
        self.wallpaper_path_0 = new_file_path
        self.save_pcman_file(0)
    
    
    def wallpaper_2_changed(self, widget):
        new_file_path = widget.get_filename()
        self.pcman_file_desktop_1 = self.pcman_file_desktop_1.replace(self.wallpaper_path_1, new_file_path)
        self.wallpaper_path_1 = new_file_path
        self.save_pcman_file(1)

# ---------------------------------------------------------------------------------------

    def set_bg_color(self, desktop):
        if desktop == 0:
            self.bg_color_0 = self.pcman_file_desktop_0.split('\n')[4].split('=')[1]
            color = Gdk.RGBA()
            color.parse(self.bg_color_0)
            self.builder.get_object('bg_color_button_1').set_rgba(color)
        elif desktop == 1:
            self.bg_color_1 = self.pcman_file_desktop_1.split('\n')[4].split('=')[1]
            color = Gdk.RGBA()
            color.parse(self.bg_color_1)
            self.builder.get_object('bg_color_button_2').set_rgba(color)
    
    def bg_color_1_changed(self, widget):
        color = widget.get_rgba().to_string()[4:][:-1]
        color = self.color_to_hex(color)
        self.pcman_file_desktop_0 = self.pcman_file_desktop_0.replace('desktop_bg=' + self.bg_color_0,
                                                                      'desktop_bg=' + color)
        self.pcman_file_desktop_0 = self.pcman_file_desktop_0.replace('desktop_shadow=' + self.bg_color_0,
                                                                      'desktop_shadow=' + color)
        
        self.bg_color_0 = color
        self.save_pcman_file(0)

            
    def bg_color_2_changed(self, widget):
        color = widget.get_rgba().to_string()[4:][:-1]
        color = self.color_to_hex(color)
        self.pcman_file_desktop_1 = self.pcman_file_desktop_0.replace('desktop_bg=' + self.bg_color_0,
                                                                      'desktop_bg=' + color)
        self.pcman_file_desktop_1 = self.pcman_file_desktop_0.replace('desktop_shadow=' + self.bg_color_0,
                                                                      'desktop_shadow=' + color)
        
        self.bg_color_1 = color
        self.save_pcman_file(1)
        
# ---------------------------------------------------------------------------------------        
    def set_fg_color(self, desktop):   
        if desktop == 0:
            self.fg_color_0 = self.pcman_file_desktop_0.split('\n')[5].split('=')[1]
            color = Gdk.RGBA()
            color.parse(self.fg_color_0)
            self.builder.get_object('fg_color_button_1').set_rgba(color)
            
        elif desktop == 1:
            self.fg_color_1 = self.pcman_file_desktop_1.split('\n')[5].split('=')[1]
            color = Gdk.RGBA()
            color.parse(self.fg_color_1)
            self.builder.get_object('fg_color_button_2').set_rgba(color)
            
    def fg_color_1_changed(self, widget):
        color = widget.get_rgba().to_string()[4:][:-1]
        color = self.color_to_hex(color)
        self.pcman_file_desktop_0 = self.pcman_file_desktop_0.replace('desktop_fg=' + self.fg_color_0,
                                                                      'desktop_fg=' + color)
        self.fg_color_0 = color
        self.save_pcman_file(0)
        
        
    def fg_color_2_changed(self, widget):
        color = widget.get_rgba().to_string()[4:][:-1]
        color = self.color_to_hex(color)
        self.pcman_file_desktop_1 = self.pcman_file_desktop_1.replace('desktop_fg=' + self.fg_color_1,
                                                                      'desktop_fg=' + color)
        self.fg_color_1 = color
        self.save_pcman_file(1)
        
# ---------------------------------------------------------------------------------------

    def color_to_hex(self, color):
        color = color.split(',')
        color_string = '#'
        for index in range(len(color)):
            hex_temp_color = hex(int(color[index]))[2:] * 2
            if len(hex_temp_color) < 4:
                hex_temp_color += hex_temp_color
            color_string += hex_temp_color
        return color_string
        
# DOCUMENTS CHECKBUTTON
# ---------------------------------------------------------------------------------
    def get_desktop_one_items(self):
        config_file = self.get_pcmanfm_file(0, False)
        file_exist = os.path.exists(config_file)
        if file_exist:
            self.pcman_file_desktop_0 = os.popen('cat {}'.format(config_file)).read()
            checkbox_documents = self.builder.get_object('checkbox_documents_monitor_1')
            checkbox_trash = self.builder.get_object('checkbox_trash_monitor_1')
            checkbox_mounts = self.builder.get_object('checkbox_mounts_monitor_1')
            
            if 'show_documents=1' in self.pcman_file_desktop_0:
                checkbox_documents.set_active(True)
            if 'show_trash=1' in self.pcman_file_desktop_0:
                checkbox_trash.set_active(True)
            if 'show_mounts=1' in self.pcman_file_desktop_0:
                checkbox_mounts.set_active(True)
                
            checkbox_documents.connect("toggled", self.checkbutton_desktop_one_items_changed)
            checkbox_trash.connect("toggled", self.checkbutton_desktop_one_items_changed)
            checkbox_mounts.connect("toggled", self.checkbutton_desktop_one_items_changed)
            
            self.set_wallpaper_mode(0)
            self.set_image_choosing_dialog(0)
            self.builder.get_object('wallpaper_laytout_combo_box_1').connect("changed", self.wallpaper_mode_1_changed)
            
            self.set_bg_color(0)
            self.builder.get_object('bg_color_button_1').connect("color-set", self.bg_color_1_changed)
            
            self.set_fg_color(0)
            self.builder.get_object('fg_color_button_1').connect("color-set", self.fg_color_1_changed)
            
            
    def get_desktop_two_items(self):
        config_file = self.get_pcmanfm_file(1, False)
        file_exist = os.path.exists(config_file)
        if file_exist:
            self.pcman_file_desktop_1 = os.popen('cat ' + config_file).read()
            checkbox_documents = self.builder.get_object('checkbox_documents_monitor_2')
            checkbox_trash = self.builder.get_object('checkbox_trash_monitor_2')
            checkbox_mounts = self.builder.get_object('checkbox_mounts_monitor_2')
            
            if 'show_documents=1' in self.pcman_file_desktop_1:
                checkbox_documents.set_active(True)  
            if 'show_trash=1' in self.pcman_file_desktop_1:
                checkbox_trash.set_active(True)    
            if 'show_mounts=1' in self.pcman_file_desktop_1:
                checkbox_mounts.set_active(True)
                
            checkbox_documents.connect("toggled", self.checkbutton_desktop_two_items_changed)
            checkbox_trash.connect("toggled", self.checkbutton_desktop_two_items_changed)
            checkbox_mounts.connect("toggled", self.checkbutton_desktop_two_items_changed)

            self.set_wallpaper_mode(1)
            self.set_image_choosing_dialog(1)
            self.builder.get_object('wallpaper_laytout_combo_box_2').connect("changed", self.wallpaper_mode_2_changed)
            
            self.set_bg_color(1)
            self.builder.get_object('bg_color_button_2').connect("color-set", self.bg_color_2_changed)

            self.set_fg_color(1)
            self.builder.get_object('fg_color_button_2').connect("color-set", self.fg_color_2_changed)
            
# ---------------------------------------------------------------------------------

    def checkbutton_desktop_one_items_changed(self, widget):
        
        if widget.get_active():
            self.pcman_file_desktop_0 = self.pcman_file_desktop_0.replace('{}=0'.format(widget.get_name()), '{}=1'.format(widget.get_name()))
        else:
            self.pcman_file_desktop_0 = self.pcman_file_desktop_0.replace('{}=1'.format(widget.get_name()), '{}=0'.format(widget.get_name()))    
        self.save_pcman_file(0)
        
    def checkbutton_desktop_two_items_changed(self, widget):
        if widget.get_active():
            self.pcman_file_desktop_1 = self.pcman_file_desktop_1.replace('{}=0'.format(widget.get_name()), '{}=1'.format(widget.get_name()))
        else:
            self.pcman_file_desktop_1 = self.pcman_file_desktop_1.replace('{}=1'.format(widget.get_name()), '{}=0'.format(widget.get_name()))    
        self.save_pcman_file(1)
    
    
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
        self.get_desktop_one_items()
        self.get_desktop_two_items()
        
        
    
    def thread_function(self):
        self.get_number_of_monitors()
        self.get_settings()
    

        
    