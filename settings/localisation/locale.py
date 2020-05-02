list_of_settings = []

# METHOD TO FIND TERRITORY AND LANGUAGE FROM LOCALE FILES
# ----------------------------------------------------------------------------
def find_in_file(path, file, territory, language):
    founded_language = founded_territory = ''
    
    with open(path + '/' + file) as file:
        line = file.readline()
        while line:
            if territory in line:
                if '%' in line:
                    line = file.readline()
                    continue
                line = line.split('"')
                founded_territory = line[1]
                
            if language in line:
                if '%' in line:
                    line = file.readline()
                    continue
                
                line = line.split('"')
                founded_language = line[1]

            line = file.readline()
    return [founded_territory, founded_language]

# METHOD TO FULFILL LIST OF SETTINGS
# -----------------------------------------------------------------------------
def fulfill_list_settings():
    global list_of_settings
    cptr = None
    with open('/usr/share/i18n/SUPPORTED') as file:
        line = file.readline()
        while line:
            if '@' in line or 'UTF-8' not in line or 'eo' in line:
                line = file.readline()
                continue
        
            temp = line.split('_')
            lang = temp[0]
            country = temp[1].replace(' ', '.')
            country = country.split('.')[0]
            if lang and country:
                cptr = '{}_{}'.format(lang, country)
                cname, lname = find_in_file("/usr/share/i18n/locales", cptr, 'territory', 'language')
                 
                list_of_settings.append([lang, country,lname,cname])
            line = file.readline()
            
# METHOD TO FULFULL COUNTRY AND LANGUAGE LISTS
# ----------------------------------------------------------------------------------------------------------------------
def fullfill_country_language():
    countries = []
    languages = []
    
    for item in list_of_settings:
        countries.append(item[3])
        languages.append(item[2])
    
    countries = list(set(countries))
    languages = list(set(languages))
    
    countries.sort()
    languages.sort()
    
    return languages, countries
    
def get_language_and_country():
    fulfill_list_settings()
    return fullfill_country_language()

def code_into_language(code):
    for locales in list_of_settings:
        if code == locales[0]:
            return locales[2]
        
def code_into_country(code):
    for locales in list_of_settings:
        if code == locales[1]:
            return locales[3]

def language_into_code(language):
    for locales in list_of_settings:
        if language in locales[2]:
            return locales[0]        
        
def country_into_code(country):
    for locales in list_of_settings:
        if country == locales[3]:
            return locales[1]       
        
        
def list_of_actual_languages(country):
    list_of_lang = []
    for item in list_of_settings:
        if country == item[3]:
            list_of_lang.append(item[2])
    return list_of_lang       
