from wifi import Cell


import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Handler:
    def __init__(self, builder):
        self.builder = builder
        
    def add_controller(self, controller):
        self.controller = controller

# METHOD TO GO NEXT
# ----------------------------------------------------------------------------------------------------------------------
    def next(self, button):
        self.controller.execute()
        #self.controller.next()

# METHOD TO GO BACK
# ----------------------------------------------------------------------------------------------------------------------
    def back(self, button):
        self.controller.back()
        
        
        
        
        
        
    def button_pressed(self, button):
        self.search()
        
        
    def search(self):
        available_networks = Cell.all('wlan0')
        print(available_networks)
        list_of_networks = []
        for item in available_networks:
            list_of_networks.append(item)
            
        wifi_tree = self.builder.get_object('wifi_tree')
        
        columns_to_remove = wifi_tree.get_columns()         #REMOVING COLUMNS IF EXIST ALREADY
        if columns_to_remove is not None:
            for column in columns_to_remove:
                wifi_tree.remove_column(column)
        
        store = Gtk.ListStore(str, bool, int)
        list_of_networks.sort(key=lambda x: x.signal)
        list_of_networks.reverse()
        for item in list_of_networks:
            store.append([item.ssid[:20], item.encrypted, item.signal])
        
        wifi_tree.set_model(store)
        
        column = Gtk.TreeViewColumn("Network")

        ssid = Gtk.CellRendererText()
        encrypted = Gtk.CellRendererText()
        signal = Gtk.CellRendererText()

        column.pack_start(ssid, True)
        column.pack_start(encrypted, True)
        column.pack_start(signal, True)

        column.add_attribute(ssid, "text", 0)
        column.add_attribute(encrypted, "text", 1)
        column.add_attribute(signal, 'text', 2)

        wifi_tree.append_column(column)
        
