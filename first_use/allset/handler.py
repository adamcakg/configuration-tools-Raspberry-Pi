import os

class Handler:
    def __init__(self, controller):
        self.controller = controller

    def on_destroy(self,button):
        os.system('reboot')
        self.controller.quit()
        

    def back(self,button):
        self.controller.back()
        
    def remove_autostart(self):
        file = os.popen('cat /etc/xdg/lxsession/LXDE-pi/autostart').read().rstrip()
        file = file.replace('@sudo python3 /etc/first_use','')
        os.popen('echo "{}" > /etc/xdg/lxsession/LXDE-pi/autostart'.format(file))
