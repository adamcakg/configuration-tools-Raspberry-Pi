
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
        
    def update(self, button):
        print('updating')
        import os
        os.system('echo {} | apt update'.format('yes'))
        os.system('echo {} | apt upgrade'.format('yes'))
        print('apt updated')
        os.system('echo {} | sudo apt dist-upgrade'.format('yes'))
        print('upgraded')
        os.system('sudo apt-get update')
        print('apt-get updated')
        self.next()
        
