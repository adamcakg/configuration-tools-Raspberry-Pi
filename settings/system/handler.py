import os

class Handler:
    def __init__(self, builder, controller=None):
        self.builder = builder
        self.changed = False
        
        self.get_hostname()

    # ADDING CONTROLLER TO HANDLER
    # ----------------------------------------------------------------------------------------------------------------------
    def add_controller(self, controller):
        self.controller = controller
        
# SETTING HOSTNAME
# ---------------------------------------------------------------
    def set_hostname(self):
        pass
        
# GETTING HOSTNAME
# ---------------------------------------------------------------
    def get_hostname(self):
        hostname = os.popen("cat /etc/hostname").read()
        print(hostname)
        self.builder.get_object("hostname_entry").set_text(hostname)
        
    def apply():
        pass