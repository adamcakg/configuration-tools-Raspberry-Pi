

class Handler:
    def __init__(self, builder, controller=None):
        self.builder = builder
        
# ADDING CONTROLLER TO HANDLER
# ----------------------------------------------------------------------------------------------------------------------        
    def add_controller(self, controller):
        self.controller = controller

    def next(self,button=None):
        self.controller.next()

    def back(self,button):
        self.controller.back()
        