from thread import Thread
import os

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

class Handler:
    def __init__(self, builder, controller=None):
        self.builder = builder
        self.set_load()
        
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
        
    def get_hardware_version(self):
        hardware_version = []
        version = os.popen('cat /proc/device-tree/model').read()
        hardware_version.append(version)
        
        other = os.popen('pinout -m | grep -oP "[A-Z]+[a-zA-Z \-()]+[:][ ][a-zA-Z0-9 ()]+"').read()
        other = other.split('\n')[:4]
        hardware_version.append(other)
        
        return hardware_version
        
    def set_hardware_version(self, version):
        self.builder.get_object('version_label').set_text(version[0])
        
        self.builder.get_object('soc_label').set_text(version[1][1].split(':')[1].lstrip())
        self.builder.get_object('ram_label').set_text(version[1][2].split(':')[1].lstrip())
        self.builder.get_object('storage_label').set_text(version[1][3].split(':')[1].lstrip())
        
    def set_load(self):
        load = os.popen('uptime | grep -oP "load average: [0-9]+[,.][0-9]+"').read().rstrip().replace('load average: ','')
        self.builder.get_object('load_label').set_text(load)
        GLib.timeout_add(500, self.set_load)
        
        
    
    def thread_function(self):
        version = self.get_os_version()
        self.set_os_version(version)
        hardware_version = self.get_hardware_version()
        self.set_hardware_version(hardware_version)
        