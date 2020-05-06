import os
from thread import Thread

class Handler:
    def __init__(self, builder, controller=None):
        self.builder = builder
        Thread(self)
    
    def add_controller(self, controller):
        self.controller = controller
        
        
    def get_available_space(self):
        storage_list = os.popen('df -h').read().rstrip().split('\n')
        for line in storage_list:
            if '/dev/root' in line:
                line = line.split()
                return line[1], line[2]
            
    def set_available_space_progressbar(self, size_of_filesystem, used_space):
        progress_bar = self.builder.get_object('progress_bar')
        progress_bar.set_text('{} used out of {}'.format(used_space, size_of_filesystem))
        
        length_of_progress_bar = float(used_space[:-1:]) / (float(size_of_filesystem[:-1:]) / 100)       
        progress_bar.set_fraction(length_of_progress_bar / 100)
                
    
    def thread_function(self):
        size_of_filesystem, used_space = self.get_available_space()
        self.set_available_space_progressbar(size_of_filesystem, used_space)
        
