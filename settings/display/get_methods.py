import os

def get_current_settings(monitor):
    current_orientation = os.popen("xrandr --verbose --screen {} | grep -oP '\) [a-z]+ \('".format(monitor-1)).read()
    current_orientation = current_orientation.rstrip()[2:][:-2]
    if current_orientation == 'normal':
        current_orientation = 0
    elif current_orientation == 'inverted':
        current_orientation = 2
    elif current_orientation == 'left':
        current_orientation = 1
    elif current_orientation == 'right':
        current_orientation = 3
        
    current_settings = os.popen("xrandr --screen {} | grep -oP '[0-9]+x[0-9]+[+][0-9][+][0-9]'".format(monitor-1)).read()
    current_settings = current_settings.rstrip().split('+')
    return current_settings[0].rstrip(), current_orientation

def get_resolutions(monitor):
    list_of_resolutions = os.popen('xrandr --screen {} | grep -oP " [0-9]+x[0-9]+ +[0-9.*+ ]+"'.format(monitor-1)).read()
    list_of_resolutions = list_of_resolutions.rstrip().split('\n')
    for index in range(len(list_of_resolutions)):
        list_of_resolutions[index] = list_of_resolutions[index].split()
    return list_of_resolutions

def get_number_of_monitors():
        monitors = (os.popen("xrandr --listmonitors | grep Monitors: | cut -d ' ' -f 2").read())[:1]
        monitors = int(monitors)
        if monitors < 2:
            return 1
        elif monitors >1:
            return 2
