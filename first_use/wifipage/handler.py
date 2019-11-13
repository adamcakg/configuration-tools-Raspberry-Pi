

class Handler:
    def __init__(self, controller):
        self.controller = controller

# METHOD TO GO NEXT
# ----------------------------------------------------------------------------------------------------------------------
    def next(self, button):
        self.controller.next()

# METHOD TO GO BACK
# ----------------------------------------------------------------------------------------------------------------------
    def back(self, button):
        self.controller.back()
    

