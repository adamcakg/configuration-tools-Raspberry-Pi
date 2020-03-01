import os
from thread import Thread

class Handler:
    def __init__(self, builder, controller=None):
        self.builder = builder
        # MEANS 0 DISABLED, 1 ENABLED
        self.original_interfaces = {'serial_port': 0, 'spi': 0, 'serial_console': 0,
                                    'camera': 0, 'vnc': 0, 'i2c': 0, '1wire': 0,
                                    'remote_gpio': 0
            }
        self.interfaces = { 'serial_port': 0, 'spi': 0, 'serial_console': 0,
                            'camera': 0, 'vnc': 0, 'i2c': 0, '1wire': 0,
                            'remote_gpio': 0
            }
        self.disable_apply_button()
        
        thread = Thread(self)

# ADDING CONTROLLER TO HANDLER
# ----------------------------------------------------------------------------------------------------------------------
    def add_controller(self, controller):
        self.controller = controller    
    
    def get_interfaces_status(self):
        # SERIAL PORT 
        if os.popen('raspi-config nonint get_serial_hw').read()[:-1] == '0':
            self.original_interfaces['serial_port'] = 1
            self.interfaces['serial_port'] = 1
            self.builder.get_object('serial_port_switch').set_active(True)
        # SPI
        if os.popen('raspi-config nonint get_spi').read()[:-1] == '0':
            self.original_interfaces['spi'] = 1
            self.interfaces['spi'] = 1
            self.builder.get_object('spi_switch').set_active(True)
        # SERIAL CONSOLE
        if os.popen('raspi-config nonint get_serial').read()[:-1] == '0':
            self.original_interfaces['serial_console'] = 1
            self.interfaces['serial_console'] = 1
            self.builder.get_object('serial_console_switch').set_active(True)
            self.builder.get_object('serial_console_switch').set_sensitive(False)
        # CAMERA
        if os.popen('raspi-config nonint get_camera').read()[:-1] == '0':
            self.original_interfaces['camera'] = 1
            self.interfaces['camera'] = 1
            self.builder.get_object('camera_switch').set_active(True)
        # VNC
        if os.popen('raspi-config nonint get_vnc').read()[:-1] == '0':
            self.original_interfaces['vnc'] = 1
            self.interfaces['vnc'] = 1
            self.builder.get_object('vnc_switch').set_active(True)
        # i2c
        if os.popen('raspi-config nonint get_i2c').read()[:-1] == '0':
            self.original_interfaces['i2c'] = 1
            self.interfaces['i2c'] = 1
            self.builder.get_object('i2c_switch').set_active(True)
        # 1WIRE
        if os.popen('raspi-config nonint get_onewire').read()[:-1] == '0':
            self.original_interfaces['1wire'] = 1
            self.interfaces['1wire'] = 1
            self.builder.get_object('1wire_switch').set_active(True)
        # REMOTE GPIO
        if os.popen('raspi-config nonint get_rgpio').read()[:-1] == '0':
            self.original_interfaces['remote_gpio'] = 1
            self.interfaces['remote_gpio'] = 1
            self.builder.get_object('remote_gpio').set_active(True)
    
    
    def connect_method_to_switches(self):
        self.builder.get_object('serial_port_switch').connect('state-set', self.switched)
        self.builder.get_object('spi_switch').connect('state-set', self.switched)
        self.builder.get_object('camera_switch').connect('state-set', self.switched)
        self.builder.get_object('vnc_switch').connect('state-set', self.switched)
        self.builder.get_object('i2c_switch').connect('state-set', self.switched)
        self.builder.get_object('1wire_switch').connect('state-set', self.switched)
        self.builder.get_object('remote_gpio_switch').connect('state-set', self.switched)
        
    def switched(self, widget, state):
        self.interfaces[widget.get_name().replace('_switch', '')] = int(state)
        if self.check_difference():
            self.disable_apply_button()
        else:
            self.enable_apply_button()
        
    def check_difference(self):
        return self.interfaces == self.original_interfaces
    
    def disable_apply_button(self):
        self.builder.get_object('apply_button').set_sensitive(False)
        
    def enable_apply_button(self):
        self.builder.get_object('apply_button').set_sensitive(True)
        
    def apply_button_clicked(self, widget):
        os.popen('sudo raspi-config nonint do_serial {}'.format(1 - self.interfaces['serial_port']))
        # SPI NOT WORKING
        #os.popen('sudo raspi-config nonint do_spi {}'.format(1 - self.interfaces['spi']))
        os.popen('sudo raspi-config nonint do_camera {}'.format(1 - self.interfaces['camera']))
        os.popen('sudo raspi-config nonint do_vnc {}'.format(1 - self.interfaces['vnc']))
        os.popen('sudo raspi-config nonint do_i2c {}'.format(1 - self.interfaces['i2c']))
        os.popen('sudo raspi-config nonint do_onewire {}'.format(1 - self.interfaces['1wire']))
        os.popen('sudo raspi-config nonint do_rgpio {}'.format(1 - self.interfaces['remote_gpio']))
        self.original_interfaces = self.interfaces 
    
    def thread_function(self):
        self.get_interfaces_status()
        self.connect_method_to_switches()
        
    
    