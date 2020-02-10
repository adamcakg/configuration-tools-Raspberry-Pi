import os

class Handler:
    def __init__(self, builder, controller=None):
        self.builder = builder
        self.what_changed = []
        
        self.set_apply_button('disable')
        
        self.get_hostname()

# ADDING CONTROLLER TO HANDLER
# ----------------------------------------------------------------------------------------------------------------------
    def add_controller(self, controller):
        self.controller = controller
        
# SETTING HOSTNAME
# ---------------------------------------------------------------
    def set_hostname(self):
        with open('/etc/hostname', 'w') as file:
            file.write(self.builder.get_object('hostname_entry').get_text() + '\n')
            
        
# GETTING HOSTNAME
# ---------------------------------------------------------------
    def get_hostname(self):
        hostname = os.popen("cat /etc/hostname").read()
        self.builder.get_object("hostname_entry").set_text(hostname[:-1])

# HOSTNAME ENTRY CHANGED
# ---------------------------------------------------------------   
    def hostname_entry_changed(self, widget):
        if 'hostname' not in self.what_changed:
            self.what_changed.append('hostname')
            self.set_apply_button('enable')
        
        
        
    def set_apply_button(self, action):
        if action == 'disable':
            self.builder.get_object("apply_button").set_sensitive(False)
        elif action == 'enable':
            self.builder.get_object("apply_button").set_sensitive(True)
        
    def apply(self, widget):
        for item in self.what_changed:
            if item == 'hostname':
                self.set_hostname()
        
        
        self.what_changed = []
        self.set_apply_button('disable')
