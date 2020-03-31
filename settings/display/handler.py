import os

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf

from thread import Thread

from .get_methods import get_current_settings, get_resolutions, get_number_of_monitors

class Handler:
    def __init__(self, builder, controller=None):
        self.builder = builder
        self.monitor_path = "/etc/settings/display/img/display1.svg"
        self.number_of_monitors = 1
        self.monitor_pressed = 1
        self.resolutions_monitor_1 = []
        self.resolutions_monitor_2 = []
        
        Thread(self)
        
# ADDING CONTROLLER TO HANDLER
# ----------------------------------------------------------------------------------------------------------------------        
    def add_controller(self, controller):
        self.controller = controller
        
    def set_monitors(self):
        if self.number_of_monitors == 1:
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(filename= self.monitor_path,
                                                             width=170, height=120, 
                                                             preserve_aspect_ratio=True)
            self.builder.get_object('monitor1').set_from_pixbuf(pixbuf)   
        else:
            self.set_picture_size(170,120,1)
            self.set_picture_size(170,120,2)
            #self.builder.get_object('display').move(widget, 0, 0)
# ----------------------------------------------------------------------------------------------------------------------        
    def get_settings(self, monitor):
        if monitor == 1:
            current_resolution, current_orientation = get_current_settings(1)
            self.resolutions_monitor_1 = get_resolutions(1)
            self.fullfil_resolutions(self.resolutions_monitor_1)
            self.set_resolution(current_resolution,1)
            self.set_frequency(current_resolution, self.resolutions_monitor_1)
            self.set_orientation(current_orientation)
            if self.number_of_monitors == 2:
                self.builder.get_object('resolution_label_monitor_2').set_label('800x600')
        else:
            current_resolution, current_orientation = get_current_settings(2)
            self.resolutions_monitor_1 = get_resolutions(2)
            self.fullfil_resolutions(self.resolutions_monitor_2)
            self.set_resolution(current_resolution, 2)
            self.set_frequency(current_resolution, self.resolutions_monitor_2)
            self.set_orientation(current_orientation)
             # TESTING
      #       self.builder.get_object('resolution_combobox_monitor_1').set_active_id('800x600')
       #      self.builder.get_object('resolution_combobox_monitor_1').connect('changed', self.resolution_changed)
        #     self.builder.get_object('frequency_combobox_monitor_1').connect('changed', self.frequency_changed)
         #    self.builder.get_object('orientation_combobox_monitor_1').connect('changed', self.orientation_changed)
             
             
            
# ----------------------------------------------------------------------------------------------------------------------            
    def fullfil_resolutions(self, resolutions):
            combobox = self.builder.get_object('resolution_combobox_monitor_1')
            combobox.remove_all()
            for resolution in resolutions:
                combobox.append(resolution[0], resolution[0])
# ---------------------------------------------------------------------------------------------------------------------- 
    def set_resolution(self, current_resolution, monitor):
            self.builder.get_object('resolution_combobox_monitor_1').set_active_id(current_resolution)
            self.builder.get_object('resolution_label_monitor_{}'.format(monitor)).set_label(current_resolution)
            self.builder.get_object('resolution_combobox_monitor_1').connect('changed', self.resolution_changed)

        
    def set_frequency(self, current_resolution, list_of_resolutions):
        active_frequency = ''
        for resolution in list_of_resolutions:
            if current_resolution == resolution[0]:
                current_resolution = resolution[1:]
        for index in range(len(current_resolution)):
            if '*' in current_resolution[index]:
                active_frequency = current_resolution[index].replace('+', '').replace('*', '')
            current_resolution[index] = current_resolution[index].replace('+', '').replace('*', '')
        combobox = self.builder.get_object('frequency_combobox_monitor_1')
        combobox.remove_all()
        for frequency in current_resolution:
            combobox.append(frequency, frequency)
        combobox.set_active_id(active_frequency)
        
        combobox.connect('changed', self.frequency_changed)
        
    def set_orientation(self, orientation):
            self.builder.get_object('orientation_combobox_monitor_1').set_active_id(str(orientation))
            self.builder.get_object('orientation_combobox_monitor_1').connect('changed', self.orientation_changed)

# ----------------------------------------------------------------------------------------------------------------------        
    def resolution_changed(self, widget):
        if self.monitor_pressed == 1:
            resolution = widget.get_active_id()
            os.popen('xrandr --screen 0 -s {} '.format(resolution))
            self.builder.get_object('resolution_label_monitor_1').set_text(resolution)
            self.builder.get_object('frequency_combobox_monitor_1').disconnect_by_func(self.frequency_changed)
            self.set_frequency(resolution, get_resolutions(1))
        else:
            resolution = widget.get_active_id()
            os.popen('xrandr --screen 1 -s {} '.format(resolution))
            self.builder.get_object('resolution_label_monitor_2').set_text(resolution)
            self.builder.get_object('frequency_combobox_monitor_1').disconnect_by_func(self.frequency_changed)
            self.set_frequency(resolution, get_resolutions(1))
        
        
    def frequency_changed(self, widget):
        if self.monitor_pressed == 1:
            os.popen('xrandr --screen 0 -r {} '.format(widget.get_active_id().replace('.', ',')))
        else:
            os.popen('xrandr --screen 1 -r {} '.format(widget.get_active_id().replace('.', ',')))
    
    def orientation_changed(self, widget):
        if self.monitor_pressed == 1:
            os.popen('xrandr --screen 0 -o {}'.format(widget.get_active_id()))
        else:
            os.popen('xrandr --screen 1 -o {}'.format(widget.get_active_id()))

# ----------------------------------------------------------------------------------------------------------------------        
    def move_picture_to_position(self, x,y, monitor):
        pass
    
    def set_picture_size(self, x, y, monitor):
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(filename= self.monitor_path,
                                                         width=x, height=y, 
                                                         preserve_aspect_ratio=True)
        if monitor == 1:
            self.builder.get_object('monitor1').set_from_pixbuf(pixbuf)
            self.builder.get_object('monitor1_event_box').set_property("width-request", x)
            self.builder.get_object('monitor1_event_box').set_property("height-request", y)
        else:
            self.builder.get_object('monitor2').set_from_pixbuf(pixbuf)
            self.builder.get_object('monitor2_event_box').set_property("width-request", x)
            self.builder.get_object('monitor2_event_box').set_property("height-request", y)
        
    def monitor_one_pressed(self, widget, state):
        print('----- Monitor 1 -------')
        self.disconnect_handlers()
        self.monitor_pressed = 1
        self.get_settings(1)
    
    def monitor_two_pressed(self, widget, state):
        print('----- Monitor 2 -------')
        self.disconnect_handlers()
        self.monitor_pressed = 2
        self.get_settings(2)
         
         
    def disconnect_handlers(self):
        self.builder.get_object('resolution_combobox_monitor_1').disconnect_by_func(self.resolution_changed)
        self.builder.get_object('frequency_combobox_monitor_1').disconnect_by_func(self.frequency_changed)
        self.builder.get_object('orientation_combobox_monitor_1').disconnect_by_func(self.orientation_changed)
    
    
    def thread_function(self):
        self.number_of_monitors = get_number_of_monitors()
        self.set_monitors()
        self.get_settings(1)
        