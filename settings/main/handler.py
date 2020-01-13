
from wifi import Wifi
from bluetooth import Bluetooth

class Handler:
    def __init__(self, builder, controller=None):
        self.builder = builder
        
# ADDING CONTROLLER TO HANDLER
# ----------------------------------------------------------------------------------------------------------------------        
    def add_controller(self, controller):
        self.controller = controller

    def go_to_wifi(self, button):
        self.controller.set_state(Wifi())
        
    def go_to_bluetooth(self, button):
        self.controller.set_state(Bluetooth())
        