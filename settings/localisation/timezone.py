import os

def get_arreas():
    timezones = os.popen('timedatectl list-timezones').read().rstrip().split('\n')
    arreas = []
    for timezone in timezones:
        arreas.append(timezone.split('/')[0])
    return list(set(arreas))

def get_locations(arrea):
    timezones = os.popen('timedatectl list-timezones').read().rstrip().split('\n')
    locations = []
    for timezone in timezones:
        if arrea in timezone:
            location = timezone.split('/')[1:]
            locations.append('/'.join(location))
    return locations