

class Handler:
    def __init__(self, builder, controller=None):
        """
            Saving builder instance for future work with page
            
        """
        self.builder = builder
        
# ADDING CONTROLLER TO HANDLER
# ----------------------------------------------------------------------------------------------------------------------        
    def add_controller(self, controller):
        """
            Adding controller instance to handler (if needed)

        """
        self.controller = controller