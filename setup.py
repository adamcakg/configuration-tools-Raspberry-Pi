import os
import sys
if len(sys.argv) < 2:
    os.popen('sudo cp -r settings/ /opt/')
    os.popen('sudo cp settings/settings.desktop /usr/share/applications/')
    print('-----------------------------------')
    print('Settings app successfully installed')
    print('To run app go to: \n\t Menu -> Preferencies -> Settings')
    print('-----------------------------------')
    os.popen('sudo cp -r first_use/ /opt/')

    print('\n\n-----------------------------------')
    print('First_start app copied')
    print('To run app type to terminal: \n\t sudo python3 /opt/first_use\n\n')
    print('When you want to run app right after reboot type: \n\t sudo setup.py -i')
elif sys.argv[1] == '-i':
    if os.popen('whoami').read().rstrip() == 'root':
        file = os.popen('cat /etc/xdg/lxsession/LXDE-pi/autostart').read().rstrip()
        file = file.replace('@sudo python3 /opt/first_use','').rstrip()
        file += '\n@sudo python3 /opt/first_use'
        os.popen('echo "{}" > /etc/xdg/lxsession/LXDE-pi/autostart'.format(file))
        print('App succesfully added...')
    else:
        print('When you want to run app right after reboot type: \n\t sudo setup.py -i')
else:
    print('Unrecognized parameter...')