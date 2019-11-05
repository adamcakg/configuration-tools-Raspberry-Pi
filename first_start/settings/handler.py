from keeper import keeper
import locale


class Handler:
    def __init__(self, builder, controller=None):
        self.controller = controller
        self.builder = builder
        
    def add_controller(self, controller):
        self.controller = controller
        
# NEXT
# ----------------------------------------------------------------------------------------------------------------------
    def next(self,button):
        self.controller.execute()
        self.controller.next()

# BACK
# ----------------------------------------------------------------------------------------------------------------------
    def back(self,button):
        self.controller.back()

# METHOD TO HANDLE COUNTRY COMBO-BOX
# ----------------------------------------------------------------------------------------------------------------------
    def country_handler(self, item):
        print('Country')
        keeper['settingspage']['country'] = item.get_active_text()
        self.insert_languages()
        self.insert_timezones()

# METHOD TO HANDLE LANGUAGE COMBO-BOX
# ----------------------------------------------------------------------------------------------------------------------
    def language_handler(self, item):
        print('language')
        keeper['settingspage']['language'] = item.get_active_text()
        
# METHOD TO HANDLE TIMEZONE COMBO-BOX
# ----------------------------------------------------------------------------------------------------------------------
    def timezone_handler(self, item):
        print('timezone')
        keeper['settingspage']['timezone'] = item.get_active_text()

# METHOD TO INSERT LANGUAGES
# ----------------------------------------------------------------------------------------------------------------------
    def insert_languages(self):
        from .settings_stuff import list_of_settings
        
        languages_object = self.builder.get_object('combo_box_language')
        languages_object.remove_all()
        
        country = self.builder.get_object('combo_box_country').get_active_text()
        
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
           countries_object.append(item, item)
           
        countries_object.set_active_id(keeper['settingspage']['country'])          
           
# METHOD TO INSERT COUNTRIES INTO TIMEZONE COMBO-BOX
# ----------------------------------------------------------------------------------------------------------------------
    def insert_timezones(self):    
        from .timezone import get_timezones_from_country
        
        timezone_object = self.builder.get_object('combo_box_timezone')
        timezone_object.remove_all()
        country = self.builder.get_object('combo_box_country').get_active_text()
        
        timezones = get_timezones_from_country(country)
        for timezone in timezones:
            timezone_object.append(timezone[1],timezone[1])
        
        timezone_in_keeper = keeper['settingspage']['timezone']
        if timezone_in_keeper in timezones:
            timezone_object.set_active_id(keeper['settingspage']['timezone'])
        else:
            timezone_object.set_active_id(timezones[0][1])
            
# METHOD FOR SETTING LOCALES ON PI
# ----------------------------------------------------------------------------------------------------------------------      
    def set_locale(self):
        from .settings_stuff import list_of_settings
        import os
        
        print('executing settings')
        #locale.setlocale(locale.LC_ALL, str('ak_GH.UTF-8'))             locales does not working, DO IT TODO
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
        
# METHOD FOR SETTING TIMEZONE ON PI
# ----------------------------------------------------------------------------------------------------------------------        
    def set_timezone(self):
        from .timezone import get_timezones_from_country
        import os
        
        country = self.builder.get_object('combo_box_country').get_active_text()
        
        print(keeper['settingspage']['timezone'])
        timezone_in_keeper = keeper['settingspage']['timezone']
        
        timezones = get_timezones_from_country(country)
        
        for timezone in timezones:
            if timezone[1] == timezone_in_keeper:
                timezone_in_keeper = timezone[0]    
        print(timezone_in_keeper)
        
        os.system('sudo timedatectl set-timezone {}'.format(timezone_in_keeper))
        os.system('sudo rm -r /etc/localtime')
        os.system("sudo dpkg-reconfigure --frontend noninteractive tzdata")
    
        
        
        
        
        


