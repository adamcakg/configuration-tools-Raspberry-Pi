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
        system('systemctl enable vncserver-x11-serviced')
        system('systemctl start vncserver-x11-serviced')

#SPI -----------------------------------------------------------------------------------------------------------------
    def spi(self):
        print('---spi')
        self.builder.get_object('software_dialog_label').set_label("Setting up SPI")
        modified_file = ''
        with open('/boot/config.txt', 'r') as file:
            line = file.readline()
            while line:
                if '#dtparam=spi=on' in line:
                    line = line.replace('#','')
                
                modified_file += line
                
                line = file.readline()
        with open('/boot/config.txt', 'w') as file:
            file.write(modified_file)

#i2c -----------------------------------------------------------------------------------------------------------------
    def i_two_c(self):
        print('---i2c')
        self.builder.get_object('software_dialog_label').set_label("Setting up I2C")
        #i2c-bcm2708
        result = popen("grep 'i2c-bcm2708' /etc/modules")
        if list(result) == []:
            popen("echo 'i2c-bcm2708' >> /etc/modules")
        #i2c-dev
        result = popen("grep 'i2c-dev' /etc/modules")
        if list(result) == []:
            popen("echo 'i2c-dev' >> /etc/modules")
        #dtparam=i2c1=on                                                                   toto pozri nenastavuje i2c
            
        result = popen("grep 'dtparam=i2c1=on' /boot/config.txt")
        if list(result) == []: 
            popen("echo 'dtparam=i2c1=on' >> /boot/config.txt")  
        #dtparam=i2c_arm=on
        result = popen("grep 'dtparam=i2c_arm=on' /boot/config.txt")
        if list(result) == []:
            popen("echo 'dtparam=i2c_arm=on' >> /boot/config.txt")
        # installing i2c-tools
        system('apt-get install -y i2c-tools')

#SERIAL -----------------------------------------------------------------------------------------------------------------
    def serial(self):
        print('---serial')
        self.builder.get_object('software_dialog_label').set_label("Setting up Serial Port")
        

