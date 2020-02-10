list_of_settings = []
countries = []
languages = []
timezone = []


# METHOD TO FIND TERRITORY AND LANGUAGE FROM LOCALE FILES
# ----------------------------------------------------------------------------------------------------------------------
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
# ----------------------------------------------------------------------------------------------------------------------
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
    global countries, languages
    
    for item in list_of_settings:
        countries.append(item[3])
        languages.append(item[2])
    
    countries = list(set(countries))
    languages = list(set(languages))
    
    countries.sort()
    languages.sort()


# METHOD TO DO THREADING
# ----------------------------------------------------------------------------------------------------------------------
def do_thread():
    fulfill_list_settings()
    fullfill_country_language()


# TESTING
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    do_thread()
    print(list_of_settings)
