from thread import Thread
import os

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf

class Handler:
    def __init__(self, builder, controller=None):
        self.builder = builder
        
        Thread(self)
        
# ADDING CONTROLLER TO HANDLER
# ----------------------------------------------------------------------------------------------------------------------        
    def add_controller(self, controller):
        self.controller = controller
        
    def get_os_version(self):
        version = []
        release = os.popen('lsb_release -a 2> /dev/null').read().split('\n')
        version.append(release[0].replace('Distributor ID:', '').lstrip())
        description = release[1].split(' ')[:3]
        description = ' '.join(description)
        version.append(description.replace('Description:', '').lstrip())
        version.append(release[2].replace('Release:', '').lstrip())
        version.append(release[3].replace('Codename:', '').lstrip())
        return version
         
    def set_os_version(self, version):
        self.builder.get_object('distributor_label').set_text(version[0])
        self.builder.get_object('description_label').set_text(version[1])
        self.builder.get_object('release_label').set_text(version[2])
        self.builder.get_object('codename_label').set_text(version[3])
    
    def thread_function(self):
        version = self.get_os_version()
        self.set_os_version(version)
        