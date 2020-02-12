import os

          
def disable_raspi_config_at_boot():
    if os.popen('[ -e /etc/profile.d/raspi-config.sh ]').read() != '':
        os.popen('rm -f /etc/profile.d/raspi-config.sh')
        if os.popen('[ -e /etc/systemd/system/getty@tty1.service.d/raspi-config-override.conf ]').read() != '':
            os.popen('rm /etc/systemd/system/getty@tty1.service.d/raspi-config-override.conf')
        os.popen('telinit q')


def set_boot_option(state, autologin):
        print(str(autologin) + '----------------------------------')
        if state == False:
            if autologin == False:
                os.popen('systemctl set-default multi-user.target')
                os.popen('ln -fs /lib/systemd/system/getty@.service /etc/systemd/system/getty.target.wants/getty@tty1.service')
                try:
                    os.popen('rm /etc/systemd/system/getty@tty1.service.d/autologin.conf')
                except:
                    print('File autologin does not exists')
            else:
                os.popen('systemctl set-default multi-user.target')
                os.popen('ln -fs /lib/systemd/system/getty@.service /etc/systemd/system/getty.target.wants/getty@tty1.service')
                os.popen('''cat > /etc/systemd/system/getty@tty1.service.d/autologin.conf << EOF
[Service]
ExecStart=
ExecStart=-/sbin/agetty --autologin $USER --noclear %I \$TERM
EOF
''')
        elif state == True:
            if autologin == False:
                os.popen('systemctl set-default graphical.target')
                os.popen('ln -fs /lib/systemd/system/getty@.service /etc/systemd/system/getty.target.wants/getty@tty1.service')
                try:
                    os.popen('rm /etc/systemd/system/getty@tty1.service.d/autologin.conf')
                except:
                    print('File autologin does not exists')
                os.popen('sed /etc/lightdm/lightdm.conf -i -e "s/^autologin-user=.*/#autologin-user=/"')
            else:
                os.popen('systemctl set-default graphical.target')
                os.popen('ln -fs /lib/systemd/system/getty@.service /etc/systemd/system/getty.target.wants/getty@tty1.service')
                print('making file autologin')
                os.popen('''cat > /etc/systemd/system/getty@tty1.service.d/autologin.conf << EOF
[Service]
ExecStart=
ExecStart=-/sbin/agetty --autologin $USER --noclear %I \$TERM
EOF
''')
                os.popen('sed /etc/lightdm/lightdm.conf -i -e "s/^\(#\|\)autologin-user=.*/autologin-user=$USER/"')

        disable_raspi_config_at_boot()




def get_boot_wait():
    try:
        open('/etc/systemd/system/dhcpcd.service.d/wait.conf')
    except:
       return 0
    return 1



if __name__ == '__main__':
    result = os.popen('[ -e /etc/profile.d/raspi-config.sh ]').read()
    print(type(result))
    print(result)
    
    os.popen('''cat > /etc/systemd/system/getty@tty1.service.d/autologin.conf << EOF
[Service]
ExecStart=
ExecStart=-/sbin/agetty --autologin $USER --noclear %I \$TERM
EOF
''')





