import os
from thread import Thread

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class Handler:
    def __init__(self, builder, controller=None):
        self.builder = builder
        self.repeat_delay = 10
        self.repeat_interval = 10
        self.beep = True
        self.left_handed = False
        self.mouse_acceleration = 0
        self.list_of_mouses = []
        
        Thread(self)

# ADDING CONTROLLER TO HANDLER
# ----------------------------------------------------------------------------------------------------------------------
    def add_controller(self, controller):
        self.controller = controller
        
# ---------------------------------------------------------------------------------------------        
    def keyboard_repeat_delay_changed(self, widget):
        self.repeat_delay = int(widget.get_value())
        os.popen('xset r rate {} {}'.format(self.repeat_delay, self.repeat_interval))
        self.builder.get_object('repeat_delay_label').set_text(str(self.repeat_delay))
         
    def set_repeat_delay(self):
        self.builder.get_object('repeat_delay_adjustment').set_value(self.repeat_delay)
        
# ---------------------------------------------------------------------------------------------         
    def keyboard_repeat_interval_changed(self, widget):
        self.repeat_interval = int(widget.get_value())
        os.popen('xset r rate {} {}'.format(self.repeat_delay, self.repeat_interval))
        self.builder.get_object('repeat_interval_label').set_text(str(self.repeat_interval))

    def set_repeat_interval(self):
        self.builder.get_object('repeat_interval_adjustment').set_value(self.repeat_interval)
# ---------------------------------------------------------------------------------------------          
    
    def beep_checkbox_changed(self, widget):
        self.beep = widget.get_active()
        os.popen('xset b {}'.format('on' if self.beep else 'off'))
    
    def set_beep(self):
        self.builder.get_object('beep_check_button').set_active(self.beep)
        
    
# ---------------------------------------------------------------------------------------------             
    def left_handed_checkbox_changed(self, widget):
        self.left_handed = widget.get_active()
        for mouse in self.list_of_mouses:
            os.popen('xinput set-prop "{}" "libinput Left Handed Enabled" {}'.format( mouse, '1' if self.left_handed else '0'))
    
    def set_left_handed(self):
        self.builder.get_object('left_handed_check_button').set_active(self.left_handed)
# ---------------------------------------------------------------------------------------------
    def mouse_acceleration_changed(self, widget):
        self.mouse_acceleration = (int(widget.get_value()) - 50 ) /50
        for mouse in self.list_of_mouses:
            os.popen('xinput set-prop "{}" "libinput Accel Speed" {} > /dev/null 2>&1'.format(mouse, str(self.mouse_acceleration)))
        
    def set_mouse_acceleration(self):
        self.builder.get_object('mouse_acceleration_adjustment').set_value(self.mouse_acceleration * 50 + 50)
        

    def mouse_double_click_delay_changed(self, widget):
        self.builder.get_object('double_click_delay_label').set_text(str(int(widget.get_value())))
        
        
# GET ALL SETTINGS OF KEYBOARD AND MOUSE
# ---------------------------------------------------------------------------------------------         
    def get_keyboard_settings(self):
        repeat_line = ''
        config = os.popen('xset q').read().split('\n')
        for line in config:
            if 'auto repeat delay:' in line:
                repeat_line = line.split()
                self.repeat_delay = int(repeat_line[3])       # delay in string
                self.repeat_interval = int(repeat_line[6])     # rate in string
        
            if 'bell percent' in line:
                bell_line = line.split()
                if int(bell_line[2]) > 0:
                    self.beep = True
                else:
                    self.beep = False
        self.set_repeat_delay()
        self.set_repeat_interval()
        self.set_beep()

    def get_mouse_settings(self):
        self.list_of_mouses = os.popen("xinput list | grep pointer | grep slave | cut -f 2 | cut -d ' ' -f 5-").read()
        self.list_of_mouses = self.list_of_mouses.split('\n')
        for mouse in range(len(self.list_of_mouses)):
            self.list_of_mouses[mouse] = self.list_of_mouses[mouse].replace('id=', '')
        self.list_of_mouses.remove('')
        self.list_of_mouses.remove('4')
        
        right_mouse_id = 0
        for mouse in self.list_of_mouses:
            if os.popen('xinput --list-props "{}" | grep "Accel Speed"'.format(mouse)).read() != '':
                right_mouse_id = mouse
        
        
        

        config = os.popen('xinput --list-props "{}"'.format(right_mouse_id)).read().split('\n')
        for line in config:
            if 'Left Handed Enabled' in line:
                line = line.split()
                if line[5] == '0':
                    self.left_handed = False
                elif line[5] == '1':
                    self.left_handed = True
            
            elif 'Accel Speed' in line:
                line = line.split()
                self.mouse_acceleration = float(line[4])
                break
                
        self.set_left_handed()
        self.set_mouse_acceleration()
        
# THREAD FUNCTION    
# ----------------------------------------------------------------------------
    def thread_function(self):
        self.get_mouse_settings()
        self.get_keyboard_settings()