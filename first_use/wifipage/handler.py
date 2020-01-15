import wifi as wifi 
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Handler:
    def __init__(self, builder):
        self.builder = builder
        self.list_of_networks = []
        self.do_in_thread = 'search'
        self.cell = None
        self.password = ''

# ADDING CONTROLLER TO HANDLER
# ---------------------------------------------------------------------------------------       
    def add_controller(self, controller):
        self.controller = controller

# METHOD TO GO NEXT
# ----------------------------------------------------------------------------------------------------------------------
    def next(self, button):
        #self.controller.execute()
        self.controller.next()

# METHOD TO GO BACK
# ----------------------------------------------------------------------------------------------------------------------
    def back(self, button):
        self.controller.back()
        
# CREATING MODAL FOR SETTING PASSWORD
# -------------------------------------------------------------------------------------------------------------
    def create_modal(self, tree, position, column):
        position = int(str(position))
        
        self.cell = self.list_of_networks[position]
        
        if self.cell:
            if self.cell.encrypted:
                print('Creating modal for entering password')
                dialog = self.builder.get_object('wifi_dialog')
                
                self.builder.get_object('connect_label').set_label('Enter the password for : "' + self.cell.ssid[:15]  + '"')
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
        pass
        # if password == None or password = '':
        #     os.popen("iwconfig " + winame + " essid " + network)
        # else:
        #     connectstatus = os.popen("iwconfig " + 'wlan0' + " essid " +cell.ssid + " key s:" + password)
        # print "Connecting..."  
        # os.popen("dhclient " + winame)
        # ontest = os.popen("ping -c 1 google.com").read()
        # print(ontest)

# SEARCHING
# -----------------------------------------------------------------------------------
    def search(self):
        print('Searching for the networks...')
        available_networks = wifi.Cell.all('wlan0')
        self.list_of_networks = []
        for item in available_networks:
            self.list_of_networks.append(item)
        
            
        wifi_tree = self.builder.get_object('wifi_tree')
        
        columns_to_remove = wifi_tree.get_columns()         #REMOVING COLUMNS IF EXIST ALREADY
        if columns_to_remove is not None:
            for column in columns_to_remove:
                wifi_tree.remove_column(column)
        
        store = Gtk.ListStore(str, bool, int)
        self.list_of_networks.sort(key=lambda x: x.signal)
        self.list_of_networks.reverse()
        for item in self.list_of_networks:
            store.append([item.ssid[:15], item.encrypted, item.signal])
        
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
        
        # HIDING SEARCHING LABEL
        self.builder.get_object('search_label').set_opacity(0)

# THREAD FUNCTION OF HANDLER
# --------------------------------------------------------------------------------------
    def thread_function(self):
        if self.do_in_thread == 'search':
            self.search()
        elif self.do_in_thread == 'connect':
            self.connect(self.cell, self.password)
