import gi
import os

from thread import Thread

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf

class Handler:
    def __init__(self, builder, controller=None):
        self.builder = builder
        self.list_of_networks = []
        self.do_in_thread = 'search'
        self.cell = None
        self.password = ''
        self.changing = False
        
        Thread(self)
        
# ADDING CONTROLLER TO HANDLER
# ----------------------------------------------------------------------------------------------------------------------        
    def add_controller(self, controller):
        self.controller = controller
        
# CREATING MODAL FOR SETTING PASSWORD
# -------------------------------------------------------------------------------------------------------------
    def create_modal(self, tree, position, column):
        position = int(str(position))
        
        self.cell = self.list_of_networks[position]
        
        if self.cell:
            if self.cell['encrypted']:
                print('Creating modal for entering password')
                dialog = self.builder.get_object('wifi_dialog')
                
                self.builder.get_object('connect_label').set_label('Enter the password for : "' + self.cell['ssid'][:15]  + '"')
                dialog.set_attached_to(self.builder.get_object('wifi'))
                dialog.set_destroy_with_parent(True)
                dialog.set_modal(True)
                dialog.show_all()
                print('modal displayed')
            else:
                self.do_in_thread = 'connect'
                Thread(self)
# DELETE MODAL
# ----------------------------------------------------------------------------------------------------------
    def delete_modal(self, button=None):
        dialog = self.builder.get_object('wifi_dialog')
        dialog.hide()
        self.cell = None
        
# REFRESH BUTTON HANDLER FOR RESEARCHING NETWORK AGAIN
# -----------------------------------------------------------------------------------------------
    def button_pressed(self, button):
        self.do_in_thread = 'search'
        Thread(self)
        
# CONNECT BUTTON HANDLER FOR CONNECTING TO NETWORK
# --------------------------------------------------------------------------------------------------
    def connect_pressed(self, button):
        self.password = self.builder.get_object('connect_entry').get_text()
        self.do_in_thread = 'connect'
        Thread(self)
        
# CONNECTING    
# ------------------------------------------------------------------------------------    
    def connect(self, cell, password=None):
        key = ''
        if cell['encrypted'] == True and cell[key] == "WPA2":
            key = "WPA-PSK"
         
        wpa2_file = os.popen("cat /etc/wpa_supplicant/wpa_supplicant.conf").read()
        
        if cell['ssid'] not in wpa2_file:
            cell = 'network={\n\tssid="'+cell["ssid"]+'"\n\tpsk="'+password+'"\n\tkey_mgmt='+key+'\n}\n'

            wpa2_file += cell

            os.popen("ifconfig wlan0 down")

            with open("/etc/wpa_supplicant/wpa_supplicant.conf", "w") as file:
                file.write(wpa2_file)
                
            os.popen("ifconfig wlan0 up")

            os.popen("wpa_cli -i wlan0 reconfigure")
        
# SEARCHING
# ----------------------------------------------------------------------------------- 
    def get_empty_cell(self):
        return {
                "ssid":"",
                "encrypted":"False",
                "quality":"",
                "key":"None"
                } 

# ----------------------------------------------------------------------------------- 
    def search(self):
        print('Searching for the networks...')
        wifi_networks = os.popen("iwlist wlan0 scan").read() 
        self.list_of_networks = [] 
         
        cell = self.get_empty_cell()
        wifi_networks = wifi_networks.split('\n')
        for list_item in wifi_networks:
            if "Quality" in list_item:
                if cell["quality"] != '':
                    self.list_of_networks.append(cell)
                    cell = self.get_empty_cell()
                cell["quality"] = list_item.strip()[-7:][:-4]
                    
            elif "Encryption key" in list_item:    
                cell["encrypted"] = "True"
            elif "ESSID:" in list_item:
                cell["ssid"] = list_item.strip()[7:][:-1]
            elif "WPA2" in list_item:
                cell["key"] = 'WPA2'
                
        if len(self.list_of_networks) == 0:
            self.builder.get_object('not_found_label').set_opacity(1)
        else:
            self.builder.get_object('not_found_label').set_opacity(0)
            self.fulfill_wifi_tree()

# ----------------------------------------------------------------------------------- 
    def fulfill_wifi_tree(self):          
        wifi_tree = self.builder.get_object('wifi_tree')
        
        columns_to_remove = wifi_tree.get_columns()         #REMOVING COLUMNS IF EXIST ALREADY
        if columns_to_remove is not None:
            for column in columns_to_remove:
                wifi_tree.remove_column(column)
        
        store = Gtk.ListStore(str, str, str)
        self.list_of_networks.sort(key=lambda x: x['quality'])
        for item in self.list_of_networks:
            if item["encrypted"]:
                encr_icon = '/etc/settings/wifi/img/lock.svg'
            else:
                encr_icon = '/etc/settings/wifi/img/none.svg'
            quality = int(item["quality"])
            print(quality)
            print(type(quality))
            if quality > -50:
                sig_icon = '/etc/settings/wifi/img/signal_high.svg'
            elif quality > -70:
                sig_icon = '/etc/settings/wifi/img/signal_medium.svg'
            else:
                sig_icon = '/etc/settings/wifi/img/signal_low.svg'
                
            store.append([item["ssid"][:15], encr_icon, sig_icon])
        
        wifi_tree.set_model(store)
        
        column = Gtk.TreeViewColumn("Network")
        column.set_alignment(0.5)
        
        name_renderer = Gtk.CellRendererText()
        column.pack_start(name_renderer, True)
        
        lock_renderer = Gtk.CellRendererPixbuf()
        column.pack_start(lock_renderer, True)
        
        signal_renderer = Gtk.CellRendererPixbuf()
        column.pack_start(signal_renderer, True)

        column.set_cell_data_func(name_renderer, self.get_tree_cell_network_name)
        column.set_cell_data_func(lock_renderer, self.get_tree_cell_lock_pixbuf)
        column.set_cell_data_func(signal_renderer, self.get_tree_cell_signal_pixbuf)
        wifi_tree.append_column(column)
        
# ---------------------------------------------------------------------------------------------------------------------- 
    def get_tree_cell_network_name(self, col, cell, model, iter, user_data):
        cell.set_property('text', model.get_value(iter, 0))

    def get_tree_cell_signal_pixbuf(self, col, cell, model, iter, user_data):
        cell.set_property('pixbuf', GdkPixbuf.Pixbuf.new_from_file_at_scale(filename=model.get_value(iter, 2),width=16, height=16, 
                                                             preserve_aspect_ratio=True))

    def get_tree_cell_lock_pixbuf(self, col, cell, model, iter, user_data):
        cell.set_property('pixbuf', GdkPixbuf.Pixbuf.new_from_file_at_scale(filename=model.get_value(iter, 1),width=16, height=16, 
                                                             preserve_aspect_ratio=True))
# ---------------------------------------------------------------------------------------------------------------------- 
    def set_widgets_to(self, state):
        self.builder.get_object('wifi_switch').set_active(state)
        self.builder.get_object('wifi_scrolled_window').set_sensitive(state)
        self.builder.get_object('refresh_button').set_sensitive(state)
            
# AIRPLANE MODE ------------------------------------------------------------------------
    def get_airplane_mode(self):
        bluetooth_state = os.popen('rfkill list bluetooth | grep -oP "Soft blocked: [a-z]+"').read().rstrip().split(' ')[-1:]
        wifi_state = os.popen('rfkill list wifi | grep -oP "Soft blocked: [a-z]+"').read().rstrip().split(' ')[-1:]
        
        if wifi_state[0] == 'no':
            self.builder.get_object('wifi_switch').set_active(True)
        
        elif bluetooth_state[0] == 'yes' and wifi_state[0] == 'yes':
            self.builder.get_object('airplane_mode_switch').set_active(True)
            return True
        elif wifi_state[0] == 'yes':
            self.builder.get_object('wifi_scrolled_window').set_sensitive(False)
            self.builder.get_object('refresh_button').set_sensitive(False)
        
        return False
    
    def set_airplane_mode(self, widget, state):
        if state:
            self.set_widgets_to(False)
            os.popen('rfkill block bluetooth')
            os.popen('rfkill block wifi')
        else:
            self.set_widgets_to(True)
            os.popen('rfkill unblock bluetooth')
            os.popen('rfkill unblock wifi')
        
# WIFI button -------------------------------------------------------------------------

    def set_wifi_button(self, widget, state):
        if state:
            os.popen('rfkill unblock wifi')
            self.set_widgets_to(True)
        else:
            os.popen('rfkill block wifi')
            self.builder.get_object('wifi_scrolled_window').set_sensitive(False)
            self.builder.get_object('refresh_button').set_sensitive(False)
            
# THREAD FUNCTION OF HANDLER
# --------------------------------------------------------------------------------------
    def thread_function(self):
        if not self.changing:
            self.changing = True
            if self.get_airplane_mode():
              self.set_widgets_to(False)
            
            if self.do_in_thread == 'search':
                self.search()
                
            elif self.do_in_thread == 'connect':
                self.connect(self.cell, self.password)
                self.delete_modal()
            self.changing = False
