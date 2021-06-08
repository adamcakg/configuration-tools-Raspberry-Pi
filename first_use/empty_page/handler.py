import os

class Handler:
    def __init__(self, controller):
        self.controller = controller

    def next(self, button):
        #self.controller,execute()
        self.controller.next()
        
    def back(self,button):
        self.controller.back()
        
