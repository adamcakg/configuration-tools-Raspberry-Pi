timezones = []
def get_timezones_db():
    global timezone
    with open("/usr/share/zoneinfo/zone.tab", "r") as file:
        line = file.readline()
        while line:
            if "#" in line:
                line = file.readline()
                continue
            line = line.split('\t')
            timezones.append(line)
            line = file.readline()

def get_timezones_from_country(country):
    from .settings_stuff import list_of_settings
    country_timezones = []
    
    for item in list_of_settings:
            if country == item[3]:
                country = item[1]
                break
    
    
    for timezone in timezones:
        if timezone[0] == country:
            country_timezones.append([timezone[2].replace('\n', ''),timezone[2].split('/')[-1].replace('_', ' ').replace('\n', '')])
    country_timezones.sort()
    
    return country_timezones

def do_threading():
    get_timezones_db()

   

