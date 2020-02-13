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


# BOOT WAIT ---------------------------------------------------------

def get_boot_wait():
    try:
        open('/etc/systemd/system/dhcpcd.service.d/wait.conf')
    except:
       return 0
    return 1

# BOOT SPLASH SCREN ---------------------------------------------------------
def get_boot_splash():
    if is_pi():
        if os.popen('grep "splash" /boot/cmdline.txt').read() == '':
            return False
        else:
            return True
    else:
        if os.popen('grep "GRUB_CMDLINE_LINUX_DEFAULT.*splash" /etc/default/grub').read() == '':
            return False
        else:
            return True

def is_pi():
    status = os.popen('dpkg --print-architecture').read()
    if 'armhf' in status:
        return True
    else:
        return False


def do_boot_splash(state):
    if os.popen('cat /usr/share/plymouth/themes/pix/pix.script').read() == '':
        return 'error'

    if state:
        if is_pi():
            if os.popen('grep "splash" /boot/cmdline.txt').read() == '': 
                os.popen('sed -i /boot/cmdline.txt -e "s/$/ quiet splash plymouth.ignore-serial-consoles/"')
        else:
            os.popen('sed -i /etc/default/grub -e "s/GRUB_CMDLINE_LINUX_DEFAULT=\"\(.*\)\"/GRUB_CMDLINE_LINUX_DEFAULT=\"\1 quiet splash plymouth.ignore-serial-consoles\"/"')
            os.popen('sed -i /etc/default/grub -e "s/  \+/ /g"')
            os.popen('sed -i /etc/default/grub -e "s/GRUB_CMDLINE_LINUX_DEFAULT=\" /GRUB_CMDLINE_LINUX_DEFAULT=\"/"')
            os.popen('update-grub')
        return 'enabled'
    else:
        if is_pi():
            if os.popen('grep "splash" /boot/cmdline.txt').read() != '':
                os.popen('sed -i /boot/cmdline.txt -e "s/ quiet//"')
                os.popen('sed -i /boot/cmdline.txt -e "s/ splash//"')
                os.popen('sed -i /boot/cmdline.txt -e "s/ plymouth.ignore-serial-consoles//"')
        else:
            os.popen('sed -i /etc/default/grub -e "s/GRUB_CMDLINE_LINUX_DEFAULT=\"\(.*\)quiet\(.*\)\"/GRUB_CMDLINE_LINUX_DEFAULT=\"\1\2\"/"')
            os.popen(' -i /etc/default/grub -e "s/GRUB_CMDLINE_LINUX_DEFAULT=\"\(.*\)splash\(.*\)\"/GRUB_CMDLINE_LINUX_DEFAULT=\"\1\2\"/"')
            os.popen('sed -i /etc/default/grub -e "s/GRUB_CMDLINE_LINUX_DEFAULT=\"\(.*\)plymouth.ignore-serial-consoles\(.*\)\"/GRUB_CMDLINE_LINUX_DEFAULT=\"\1\2\"/"')
            os.popen('sed -i /etc/default/grub -e "s/  \+/ /g"')
            os.popen('sed -i /etc/default/grub -e "s/GRUB_CMDLINE_LINUX_DEFAULT=\" /GRUB_CMDLINE_LINUX_DEFAULT=\"/"')
            os.popen('update-grub')
        return 'disabled'


# TESTING --------------------------------------------------------------------
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





