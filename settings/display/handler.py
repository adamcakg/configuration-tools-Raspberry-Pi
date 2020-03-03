import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf

class Handler:
    def __init__(self, builder, controller=None):
        self.builder = builder
        self.monitor_path = "display/img/display1.svg"
        
# ADDING CONTROLLER TO HANDLER
# ----------------------------------------------------------------------------------------------------------------------        
    def add_controller(self, controller):
        self.controller = controller
    
    def set_picture_size(self, x, y, monitor):
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
        filename= self.monitors,
        width=x, 
        height=y, 
        preserve_aspect_ratio=True)
        if monitor == 1:
            self.builder.get_object('monitor1').set_from_pixbuf(pixbuf)
        else:
            self.builder.get_object('monitor2').set_from_pixbuf(pixbuf)
        
        
        
    def set_position(self, widget):
        pass
        
        
        #self.builder.get_object('display').move(widget, 0, 0)
        