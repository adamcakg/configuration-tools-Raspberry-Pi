
class Handler:
    def __init__(self, builder):
        self.builder = builder
        self.switches = ['ssh','vnc','spi', 'i2c', 'gpio']
        
# ADDING CONTROLLER TO HANDLER
# ----------------------------------------------------------------------------------------------------------------------        
    def add_controller(self, controller):
        self.controller = controller
        

    def next(self,button):
        self.controller.execute()
        self.controller.next()

    def back(self, button):
        self.controller.back()
        
    def get_list_of_active_switches(self):
        active_switches = []
        for switch in self.switches:
            if self.builder.get_object('switch_software_{}'.format(switch)).get_active():
                active_switches.append(switch)
                
        return active_switches

    
    def turn_on_functions(self, list_of_functions):
        for function in list_of_functions:
            if function == 'ssh':
                self.ssh()
            elif function == 'vnc':
                self.vnc()
            elif function == 'spi':
                self.spi()
            elif function == 'i2c':
                self.i_two_c()
            elif function == 'gpio':
                self.gpio()
            
# FUNCTION TO SET UP
# ---------------------------------------------------------------------------------------------------------------------

    def ssh(self):
        print('ssh')
        
    def vnc(self):
        print('vnc')
        
    def spi(self):
        print('spi')
        
    def i_two_c(self):
        print('i2c')
        
    def gpio(self):
        print('gpio')

