from thread import Thread
import os

from .keyboard_list import get_keyboard_stuff
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Handler:
    def __init__(self, builder, controller=None):
        self.builder = builder
        self.option = None
        self.language_store = None
        self.country = []
        
        thread = Thread(self)
        
      

# ADDING CONTROLLER TO HANDLER
# ----------------------------------------------------------------------------------------------------------------------
    def add_controller(self, controller):
        self.controller = controller
# ----------------------------------------------------------------------------------------------------------------------    
    def fullfil_keyboard_combo_boxes(self, models, layouts, variants):
        model_combo_box = self.builder.get_object('model_combo_box')
        for model in models:
            model_combo_box.append(model[1].lstrip(), model[0][:35])
            
        current_model = os.popen("grep XKBMODEL /etc/default/keyboard | cut -d = -f 2 | tr -d '\"' | rev | cut -d , -f 1 | rev")
        current_model = current_model.read().rstrip()
        if current_model == '':
            model_combo_box.set_active(0)
        else:
            model_combo_box.set_active_id(current_model)
            
        layout_combo_box = self.builder.get_object('layout_combo_box')
        for layout in layouts:
            layout_combo_box.append(layout[1].lstrip(), layout[0][:35])
            
        current_layout = os.popen("grep XKBLAYOUT /etc/default/keyboard | cut -d = -f 2 | tr -d '\"' | rev | cut -d , -f 1 | rev")
        current_layout = current_layout.read()
        layout_combo_box.set_active_id(current_layout.rstrip())
        
    
    def set_up_variant_combo_box(self, widget):
        variant_combo_box = self.builder.get_object('variant_combo_box')
        variant_combo_box.remove_all()
        variant_combo_box.append(widget.get_active_id(), widget.get_active_text()[:35])
        try:
            for item in self.variants[widget.get_active_id()]:
                variant_combo_box.append(item[1].lstrip(),item[0][:35])
            current_variant = os.popen("grep XKBVARIANT /etc/default/keyboard | cut -d = -f 2 | tr -d '\"' | rev | cut -d , -f 1 | rev")
            current_variant = current_variant.read().rstrip()
            if current_variant == '':
                variant_combo_box.set_active(0)
            else:
                layout = self.builder.get_object('layout_combo_box').get_active_id()
                for item in self.variants[layout]:
                    if item[1].lstrip() == current_variant:
                        variant_combo_box.set_active_id(current_variant)
                        return
                variant_combo_box.set_active(0)
            
        except Exception:
            variant_combo_box.set_active_id(widget.get_active_id())
        
    def change_keyboard(self, widget):
        self.delete_keyboard_modal()
        model = self.builder.get_object('model_combo_box').get_active_id()
        command = "grep -q XKBMODEL /etc/default/keyboard && sudo sed -i 's/XKBMODEL=.*/XKBMODEL="
        command += "{}/g' /etc/default/keyboard || sudo echo 'XKBMODEL={}' >> /etc/default/keyboard".format(model, model)
        os.popen(command)
        
        layout = self.builder.get_object('layout_combo_box').get_active_id()
        command = "grep -q XKBLAYOUT /etc/default/keyboard && sudo sed -i 's/XKBLAYOUT=.*/XKBLAYOUT="
        command += "{}/g' /etc/default/keyboard || sudo echo 'XKBLAYOUT={}' >> /etc/default/keyboard".format(layout, layout)
        os.popen(command)
        
        variant = self.builder.get_object('variant_combo_box').get_active_id()
        if variant == layout:
            variant = "''"
        command = "grep -q XKBVARIANT /etc/default/keyboard && sudo sed -i 's/XKBVARIANT=.*/XKBVARIANT="
        command += "{}/g' /etc/default/keyboard || sudo echo 'XKBVARIANT={}' >> /etc/default/keyboard".format('' if variant== "''" else variant, '' if variant== "''" else variant)
        os.popen(command)
    
        os.popen("setxkbmap {} {} {} {} {} {}".format('-model', model, '-layout', layout, '-variant', variant))
        
    def create_keyboard_modal(self, widget):
        dialog = self.builder.get_object('keyboard_modal')
        dialog.set_attached_to(self.builder.get_object('accessibility'))
        dialog.show_all()
    
    def delete_keyboard_modal(self, widget=None):
        dialog = self.builder.get_object('keyboard_modal')
        dialog.hide()
    

# ----------------------------------------------------------------------------------------------------------------------




    
    def create_timezone_modal(self):
        pass
    
    
    
    def create_country_modal(self):
        pass

    def delete_localisation_modal(self, widget=None):
        dialog = self.builder.get_object('localisation_modal')
        dialog.hide()
    
    
    def change_option_in_localisation(self, widget):
        pass
    
    
    
    
        
    def thread_function(self):
        self.models, self.layouts, self.variants = get_keyboard_stuff()
        self.fullfil_keyboard_combo_boxes(self.models, self.layouts, self.variants)
        
        
        