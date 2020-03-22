from os import system, popen

class Handler:
    def __init__(self, builder):
        self.builder = builder
        self.switches = ['ssh','vnc','spi', 'i2c', 'serial']
        
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
            elif function == 'serial':
                self.serial()
                
    def thread_function(self):
        active_switches = self.get_list_of_active_switches()
        self.turn_on_functions(active_switches)
        
# MODAL
# ---------------------------------------------------------------------------------------------------------------
    def create_modal(self):
        print('modal function')
        dialog = self.builder.get_object('software_dialog')
        dialog.set_attached_to(self.builder.get_object('software_page'))
        dialog.set_destroy_with_parent(True)
        dialog.set_modal(True)
        dialog.show_all()
        print('modal displayed')
        
    def delete_modal(self):
        dialog = self.builder.get_object('software_dialog')
        dialog.destroy()
        
# FUNCTION TO SET UP
# ---------------------------------------------------------------------------------------------------------------------
#SSH -----------------------------------------------------------------------------------------------------------------
    def ssh(self):
        print('---ssh')
        self.builder.get_object('software_dialog_label').set_label("Setting up SSH")
        system('systemctl enable ssh')
        system('systemctl start ssh')

#VNC -----------------------------------------------------------------------------------------------------------------
    def vnc(self):
        print('---vnc')
        self.builder.get_object('software_dialog_label').set_label("Setting up VNC")
        popen('sudo raspi-config nonint do_vnc 0')

#SPI -----------------------------------------------------------------------------------------------------------------
    def spi(self):
        print('---spi')
        self.builder.get_object('software_dialog_label').set_label("Setting up SPI")
        # SPI NOT WORKING
        #popen('sudo raspi-config nonint do_spi 0')

#i2c -----------------------------------------------------------------------------------------------------------------
    def i_two_c(self):
        print('---i2c')
        popen('sudo raspi-config nonint do_i2c 0')
        
#SERIAL -----------------------------------------------------------------------------------------------------------------
    def serial(self):
        print('---serial')
        self.builder.get_object('software_dialog_label').set_label("Setting up Serial Port")
        popen('sudo raspi-config nonint do_serial 0')

