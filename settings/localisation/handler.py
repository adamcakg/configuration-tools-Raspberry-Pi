from thread import Thread
import os

from .keyboard_list import get_keyboard_stuff
from .locale import get_language_and_country, list_of_settings, code_into_language, code_into_country
from .locale import list_of_actual_languages, language_into_code, country_into_code
from .timezone import get_arreas, get_locations

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Handler:
    def __init__(self, builder, controller=None):
        self.builder = builder
        self.option = None
        self.language_store = None
        self.country = []
        self.what_to_do = 'get_settings'
        
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
        dialog.set_attached_to(self.builder.get_object('localisation'))
        dialog.show_all()
    
    def delete_keyboard_modal(self, widget=None):
        dialog = self.builder.get_object('keyboard_modal')
        dialog.hide()
    
# ----------------------------------------------------------------------------------------------------------------------
    def fullfil_languages(self, widget=None):
        country = self.builder.get_object('country_combo_box').get_active_id()
        language_combo_box = self.builder.get_object('language_combo_box')
        language_combo_box.remove_all()
        
        list_of_languages = list_of_actual_languages(country)
        for language in list_of_languages:
            language_combo_box.append(language, language)
            
        current_settings = os.popen('localectl status | grep -oP [a-z]+_[A-Z]+.[A-Za-z0-9-:]+').read()
        current_code = current_settings.split('_')[0]
        current_language = code_into_language(current_code)
        
        for language in list_of_languages:
            if current_language in language:
                language_combo_box.set_active_id(language)
                return
        language_combo_box.set_active_id(list_of_languages[0])
        
    def fullfil_countries(self, countries):
        countries_combo_box = self.builder.get_object('country_combo_box')
        for country in countries:
           countries_combo_box.append(country, country[:22])
        
        current_settings = os.popen('localectl status | grep -oP [a-z]+_[A-Z]+.[A-Za-z0-9-:]+').read()
        current_code = current_settings.split('_')[1].split('.')[0]
        countries_combo_box.set_active_id(code_into_country(current_code))
    
    def change_locale(self, widget):
        self.delete_localisation_modal()
        self.what_to_do = 'set_locale'
        
        thread = Thread(self)
        self.create_setting_modal('Setting locale')
    
    def set_locale(self):
        language = self.builder.get_object('language_combo_box').get_active_id()
        country = self.builder.get_object('country_combo_box').get_active_id()
            
        language_code = language_into_code(language)
        country_code = country_into_code(country)
        self.change_progress_bar(10)
        os.system("sudo sed -i /etc/locale.gen -e 's/^\\([^#].*\\)/# \\1/g'")
        self.change_progress_bar(40)
        os.system("sudo sed -i /etc/locale.gen -e 's/^# \\({}_{}[\\. ].*UTF-8\\)/\\1/g'".format(language_code, country_code))
        self.change_progress_bar(70)
        os.system("sudo locale-gen")
        self.change_progress_bar(90)
        command = "sudo LC_ALL={0}_{1}{2} LANG={0}_{1}{2} LANGUAGE={0}_{1}{2} update-locale LANG={0}_{1}{2}  LC_ALL={0}_{1}{2} LANGUAGE={0}_{1}{2}"
        os.system(command.format(language_code, country_code, '.UTF-8'))
                                                                                                                                                                                                                                                                                        
        self.change_progress_bar(100)
        self.hide_setting_modal()
        self.builder.get_object('reboot_label').set_opacity(1)
        self.builder.get_object('reboot_button').set_opacity(1)
        self.builder.get_object('reboot_button').set_sensitive(1)
    
       
    def create_localisation_modal(self, widget):
        dialog = self.builder.get_object('localisation_modal')
        dialog.set_attached_to(self.builder.get_object('localisation'))
        dialog.show_all()

    def delete_localisation_modal(self, widget=None):
        dialog = self.builder.get_object('localisation_modal')
        dialog.hide()
# ----------------------------------------------------------------------------------------------------------------------    
    def fulfill_arreas(self, arreas):
        arrea_combo_box = self.builder.get_object('arrea_combo_box')
        for arrea in arreas:
            arrea_combo_box.append(arrea, arrea)
        current_timezone = os.popen('timedatectl show | grep -oP [A-Za-z]+\/[a-zA-Z_]+').read().rstrip()
        current_arrea = current_timezone.split('/')[0]
        arrea_combo_box.set_active_id(current_arrea)
        
    
    def fulfill_locations(self, widget=None):    
        arrea = self.builder.get_object('arrea_combo_box').get_active_id()
        locations = get_locations(arrea)
        location_combo_box = self.builder.get_object('location_combo_box')
        location_combo_box.remove_all()
        for location in locations:
            location_combo_box.append(location, location)
            
        current_timezone = os.popen('timedatectl show | grep -oP [A-Za-z]+\/[a-zA-Z_]+').read().rstrip()
        current_location = current_timezone.split('/')[1:]
        current_location = '/'.join(current_location)
        
        if locations == ['']:
            return
        elif len(locations) == 1:
            location_combo_box.set_active_id(locations[0])
        elif current_location in locations:
            location_combo_box.set_active_id(current_location)
        else:
            location_combo_box.set_active_id(locations[9])
    
    def set_timezone(self, widget):
        self.delete_timezone_modal()
        arrea = self.builder.get_object('arrea_combo_box').get_active_id()
        location = self.builder.get_object('location_combo_box').get_active_id()
        
        os.popen('sudo timedatectl set-timezone {}/{}'.format(arrea, location))
    
    def create_timezone_modal(self, widget):
        dialog = self.builder.get_object('timezone_modal')
        dialog.set_attached_to(self.builder.get_object('localisation'))
        dialog.show_all()

    def delete_timezone_modal(self, widget=None):
        dialog = self.builder.get_object('timezone_modal')
        dialog.hide()
# ----------------------------------------------------------------------------------------------------------------------       
    def fullfil_wifi_countries(self, countries):
        country_combo_box = self.builder.get_object('wifi_country_combo_box')
        for country in countries:
            country_combo_box.append(country, country)
        current_country_code = os.popen('raspi-config nonint get_wifi_country').read().rstrip()
        if current_country_code == '':
            country_combo_box.set_active_id('United Kingdom')
        else:
            current_country = code_into_country(current_country_code)
            country_combo_box.set_active_id(current_country)

    def set_wifi_country(self, widget):
        self.hide_wifi_country_modal()
        selected_country = self.builder.get_object('wifi_country_combo_box').get_active_id()
        country_code = country_into_code(selected_country)
        
        os.popen('raspi-config nonint do_wifi_country {}'.format(country_code))
        
        
    
    def create_wifi_country_modal(self, widget):
        dialog = self.builder.get_object('wifi_country_modal')
        dialog.set_attached_to(self.builder.get_object('localisation'))
        dialog.show_all()

    def hide_wifi_country_modal(self, widget=None):
        dialog = self.builder.get_object('wifi_country_modal')
        dialog.hide()
    

# ----------------------------------------------------------------------------------------------------------------------   
    def create_setting_modal(self, what_setting):
        self.builder.get_object("setting_label").set_text(what_setting)
        dialog = self.builder.get_object('setting_modal')
        dialog.set_attached_to(self.builder.get_object('localisation'))
        dialog.show_all()

    def hide_setting_modal(self):
        dialog = self.builder.get_object('setting_modal')
        dialog.hide()

    def change_progress_bar(self, percentage):
        self.builder.get_object('progress_bar').set_fraction(percentage/100)
# ----------------------------------------------------------------------------------------------------------------------           
    def reboot(self, widget):
        os.system('reboot')

# ----------------------------------------------------------------------------------------------------------------------   
    def thread_function(self):
        
        if self.what_to_do == 'get_settings':
            languages, countries = get_language_and_country()
            self.fullfil_countries(countries)
            self.fullfil_languages()
            
            self.fulfill_arreas(get_arreas())
            self.fulfill_locations()
            
            self.models, self.layouts, self.variants = get_keyboard_stuff()
            self.fullfil_keyboard_combo_boxes(self.models, self.layouts, self.variants)
            
            self.fullfil_wifi_countries(countries)
            
        elif self.what_to_do == 'set_locale':   
            self.set_locale()
            
            
        