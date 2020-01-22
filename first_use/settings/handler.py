from keeper import keeper
import locale

from .settings_stuff import list_of_settings
from .timezone import get_timezones_from_country
import os


class Handler:
    def __init__(self, builder):
        self.builder = builder
        
# ADDING CONTROLLER TO HANDLER
# ----------------------------------------------------------------------------------------------------------------------        
    def add_controller(self, controller):
        self.controller = controller
        
# NEXT
# ----------------------------------------------------------------------------------------------------------------------
    def next(self,button):    
        self.controller.execute()

# BACK
# ----------------------------------------------------------------------------------------------------------------------
    def back(self,button):
        self.controller.back()

# METHOD TO HANDLE COUNTRY COMBO-BOX
# ----------------------------------------------------------------------------------------------------------------------
    def country_handler(self, item):
        keeper['settingspage']['country'] = item.get_active_id()
        self.insert_languages()
        self.insert_timezones()

# METHOD TO HANDLE LANGUAGE COMBO-BOX
# ----------------------------------------------------------------------------------------------------------------------
    def language_handler(self, item):
        keeper['settingspage']['language'] = item.get_active_text()
        
# METHOD TO HANDLE TIMEZONE COMBO-BOX
# ----------------------------------------------------------------------------------------------------------------------
    def timezone_handler(self, item):
        keeper['settingspage']['timezone'] = item.get_active_text()

# METHOD TO INSERT LANGUAGES
# ----------------------------------------------------------------------------------------------------------------------
    def insert_languages(self):
        languages_object = self.builder.get_object('combo_box_language')
        languages_object.remove_all()
        
        country = self.builder.get_object('combo_box_country').get_active_id()
        
        lang_in_keeper = keeper['settingspage']['language']
        list_of_lang = []
        for item in list_of_settings:
            if country == item[3]:
                list_of_lang.append(item[2])
                languages_object.append(item[2],item[2])
        
        if lang_in_keeper in list_of_lang:
            languages_object.set_active_id(lang_in_keeper)
        else:
            languages_object.set_active_id(list_of_lang[0])

# METHOD TO INSERT COUNTRIES INTO COUNTRY COMBO-BOX
# ----------------------------------------------------------------------------------------------------------------------
    def insert_countries(self):
        countries_object = self.builder.get_object('combo_box_country')

        from .settings_stuff import countries
        
        for item in countries:
           countries_object.append(item, item[:22])
           
        countries_object.set_active_id(keeper['settingspage']['country'])          
           
# METHOD TO INSERT COUNTRIES INTO TIMEZONE COMBO-BOX
# ----------------------------------------------------------------------------------------------------------------------
    def insert_timezones(self):            
        timezone_object = self.builder.get_object('combo_box_timezone')
        timezone_object.remove_all()
        country = self.builder.get_object('combo_box_country').get_active_id()
        
        timezones = get_timezones_from_country(country)
        for timezone in timezones:
            timezone_object.append(timezone[1],timezone[1])
        
        timezone_in_keeper = keeper['settingspage']['timezone']
        if timezone_in_keeper in timezones:
            timezone_object.set_active_id(keeper['settingspage']['timezone'])
        else:
            timezone_object.set_active(0)
            
# SETTING TIMEZONE
# --------------------------------------------------------------------------------------------------
    def set_timezone(self):
        country = self.builder.get_object('combo_box_country').get_active_text()
        
        print(keeper['settingspage']['timezone'])
        timezone_in_keeper = keeper['settingspage']['timezone']
        
        timezones = get_timezones_from_country(country)
        
        for timezone in timezones:
            if timezone[1] == timezone_in_keeper:
                timezone_in_keeper = timezone[0]    
        print(timezone_in_keeper)
        
        os.system(f'sudo timedatectl set-timezone {timezone_in_keeper}')
        os.system('sudo rm -r /etc/localtime')
        os.system("sudo dpkg-reconfigure --frontend noninteractive tzdata")
    
# SETTING LOCALES
# ------------------------------------------------------------------------------------------------------
    def set_locale(self):
        """
        SETTING LOCALES
        """
        #locale.setlocale(locale.LC_ALL, str('ak_GH.UTF-8'))            
        print('Locale before set + ' + str(locale.getlocale()))
        
        lang = keeper['settingspage']['language']
        count = keeper['settingspage']['country']
        for locales in list_of_settings:
            if count == locales[3]:
                if lang == locales[2]:
                    lang = locales[0]
                    count = locales[1]
                    break
        
        os.system("sudo sed -i /etc/locale.gen -e 's/^\\([^#].*\\)/# \\1/g'")
        os.system("sudo sed -i /etc/locale.gen -e 's/^# \\({}_{}[\\. ].*UTF-8\\)/\\1/g'".format(lang, count))
        os.system("sudo locale-gen")
        os.system("sudo LC_ALL={0}_{1}{2} LANG={0}_{1}{2} LANGUAGE={0}_{1}{2} update-locale LANG={0}_{1}{2}  LC_ALL={0}_{1}{2} LANGUAGE={0}_{1}{2} ".format(lang, count,'.UTF-8'))
       
        print('Locale was set + ' + str(locale.getlocale()))
        
            
# THREAD FUNCTION TO SET LOCALE AND TIMEZONE
# ----------------------------------------------------------------------------------------------------------------------      
    def thread_function(self):
        self.set_timezone()
        self.set_locale()
        
# MODAL
# ----------------------------------------------------------------------------------------------------------------------        
    def create_modal(self):
        print('modal function')
        dialog = self.builder.get_object('settings_dialog')
        dialog.set_attached_to(self.builder.get_object('settings'))
        dialog.set_destroy_with_parent(True)
        dialog.set_modal(True)
        dialog.show_all()
        print('modal displayed')
        
    def delete_modal(self):
        dialog = self.builder.get_object('settings_dialog')
        dialog.destroy()
        self.controller.next()




