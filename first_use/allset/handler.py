import os

class Handler:
    def __init__(self, controller):
        self.controller = controller

    def on_destroy(self,button):
        os.system('reboot')
        self.controller.quit()
        

    def back(self,button):
        self.controller.back()
