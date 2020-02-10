import gi
import os

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Handler:
    def __init__(self, builder, controller=None):
        self.builder = builder
        self.list_of_networks = []
        self.do_in_thread = 'search'
        self.cell = None
        self.password = ''
        
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
                self.controller.execute()
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
        self.controller.execute()
        
# CONNECT BUTTON HANDLER FOR CONNECTING TO NETWORK
# --------------------------------------------------------------------------------------------------
    def connect_pressed(self, button):
        self.password = self.builder.get_object('connect_entry').get_text()
        self.do_in_thread = 'connect'
        self.controller.execute()
        
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
                       
    def fulfill_wifi_tree(self):          
        wifi_tree = self.builder.get_object('wifi_tree')
        
        columns_to_remove = wifi_tree.get_columns()         #REMOVING COLUMNS IF EXIST ALREADY
        if columns_to_remove is not None:
            for column in columns_to_remove:
                wifi_tree.remove_column(column)
        
        store = Gtk.ListStore(str, str, str)
        self.list_of_networks.sort(key=lambda x: x['quality'])
        for item in self.list_of_networks:
            store.append([item["ssid"][:15], item["encrypted"], item["quality"]])
        
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

# THREAD FUNCTION OF HANDLER
# --------------------------------------------------------------------------------------
    def thread_function(self):
        if self.do_in_thread == 'search':
            self.search()
        elif self.do_in_thread == 'connect':
            self.connect(self.cell, self.password)
            self.delete_modal()
            
# AIRPLANE MODE ------------------------------------------------------------------------
    
    def set_airplane_mode(self):
        # todo
        pass    

# WIFI button -------------------------------------------------------------------------

    def set_wifi_button(self):
        #todo    rfkill list

        pass
        




