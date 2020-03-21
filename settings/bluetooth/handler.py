from thread import Thread
import os
import time
from .bluetoothctl import Bluetoothctl

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf

class Handler:
    def __init__(self, builder, controller=None):
        self.builder = builder
        self.bluetooth = None
        self.what_to_do = 'check'
        Thread(self)
        
# ADDING CONTROLLER TO HANDLER
# ----------------------------------------------------------------------------------------------------------------------        
    def add_controller(self, controller):
        self.controller = controller
    
# ----------------------------------------------------------------------------------------------------------------------    
    def fulfill_devices(self):
        devices = self.bluetooth.get_discoverable_devices()
        paired_devices = self.bluetooth.get_paired_devices()
        if devices == [] or devices == None:
            return
        
        tree = self.builder.get_object('bluetooth_tree')
        
        columns_to_remove = tree.get_columns()         #REMOVING COLUMNS IF EXIST ALREADY
        if columns_to_remove is not None:
            for column in columns_to_remove:
                tree.remove_column(column)
        
        store = Gtk.ListStore(str, str)
        tree.set_model(store)
        
        for paired in paired_devices:
            store.append(["bluetooth/img/bluetooth.svg", paired['name']])                 #TO DO : CHANGE TO RED IF PAIRED 
        
        for device in devices:
            store.append(["bluetooth/img/bluetooth.svg", device['name']])
        
        px_column = Gtk.TreeViewColumn('Devices')
        px_renderer = Gtk.CellRendererPixbuf()
            
        px_column.pack_start(px_renderer, False)
        str_renderer = Gtk.CellRendererText()
        px_column.pack_start(str_renderer, False)

        px_column.set_cell_data_func(px_renderer, self.get_tree_cell_pixbuf)
        px_column.set_cell_data_func(str_renderer, self.get_tree_cell_text)
        tree.append_column(px_column)

# ---------------------------------------------------------------------------------------------------------------------- 
    def get_tree_cell_text(self, col, cell, model, iter, user_data):
        cell.set_property('text', model.get_value(iter, 1))


    def get_tree_cell_pixbuf(self, col, cell, model, iter, user_data):
        cell.set_property('pixbuf', GdkPixbuf.Pixbuf.new_from_file_at_scale(filename=model.get_value(iter, 0),width=32, height=32, 
                                                             preserve_aspect_ratio=True))

# ---------------------------------------------------------------------------------------------------------------------- 
    def check_state(self):
        state = os.popen('rfkill list bluetooth | grep -oP "Soft blocked: [a-z]+"').read().rstrip().split(' ')[-1:]
        self.builder.get_object('bluetooth_switch').set_active(True if state[0]=='no' else False)
        self.builder.get_object('bluetooth_switch').connect('state-set', self.state_changed)
        return state[0]

# ---------------------------------------------------------------------------------------------------------------------- 
    def set_widgets_to(self, state):
        self.builder.get_object('refresh_button').set_sensitive(state)
        self.builder.get_object('scrolled_window').set_sensitive(state)
        self.builder.get_object('discoverable_button').set_sensitive(state)

# ---------------------------------------------------------------------------------------------------------------------- 
    def state_changed(self, widget, state):
        if not state:
            os.popen('rfkill block bluetooth')
            self.set_widgets_to(False)
        else:
            self.bluetooth = Bluetoothctl()
            self.set_widgets_to(True)
            self.bluetooth.start_scan()
            self.fulfill_devices()
    
# ----------------------------------------------------------------------------------------------------------------------     
    def create_modal_of_device(self, widget):
        pass
    
    
# ----------------------------------------------------------------------------------------------------------------------   
    def set_discoverable(self, widget):
        self.bluetooth.make_discoverable()
        widget.set_sensitive(False)
        self.what_to_do = 'disable discoverable'
        Thread(self)
    
# ----------------------------------------------------------------------------------------------------------------------     
    def thread_function(self):
        if self.what_to_do == 'check':
            is_off = self.check_state()
            if is_off == 'yes':
                self.set_widgets_to(False)
            else:
                self.bluetooth = Bluetoothctl()
                self.bluetooth.start_scan()
                self.fulfill_devices()
        
        elif self.what_to_do == 'disable discoverable':
            time.sleep(15)
            self.bluetooth.stop_discoverable()
            try:
                self.builder.get_object('discoverable_button').set_sensitive(True)
            except Exception:
                return
    