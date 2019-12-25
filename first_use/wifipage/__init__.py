import update_page as update_page
import passwordpage as password_page
from .handler import Handler

from wifi import Cell  

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib


class WifiPage:
    def __init__(self):
        self.__builder = Gtk.Builder()                  # Initializing builder
        self.__builder.add_from_file('wifipage/wifi.glade')   # creating object from XML(.glade files)
        self.search()


# METHOD TO GO NEXT
# ----------------------------------------------------------------------------------------------------------------------
    def next(self, controller):
        controller.set_state(update_page.UpdatePage())

# METHOD TO GO BACK
# ----------------------------------------------------------------------------------------------------------------------
    def back(self, controller):
        controller.set_state(password_page.PasswordPage())

# METHOD TO GET XML OBJECT
# ----------------------------------------------------------------------------------------------------------------------
    def get_xml_object(self):
        return self.__builder.get_object('wifi')

# METHOD TO DESTROY ITSELF
# ----------------------------------------------------------------------------------------------------------------------
    def destroy(self):
        del self

# METHOD TO CONNECT HANDLER
# ----------------------------------------------------------------------------------------------------------------------
    def connect_handler(self, controller):
        self.__builder.connect_signals(Handler(controller))

# METHOD TO EXECUTE PAGE
# ----------------------------------------------------------------------------------------------------------------------
    def execute(self):
        pass
    
    def search(self):
        available_networks = Cell.all('wlan0')
        print(available_networks)
        list_of_networks = []
        for item in available_networks:
            list_of_networks.append(item)
            
        wifi_tree = self.__builder.get_object('wifi_tree')
        
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
        
        
        
