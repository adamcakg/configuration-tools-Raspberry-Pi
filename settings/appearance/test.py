 
    def check_dir(path):
        GLib.mkdir_with_parents(path, 6)
        
# ---------------------------------------------------------------------------------------
        
    def get_openbox_file(self):
        filename = GLib.getenv ("DESKTOP_SESSION").lower() + '-rc.xml'
        path = GLib.get_user_config_dir() + '/openbox/' + filename
        return path
    
# ---------------------------------------------------------------------------------------    
    def get_lxsession_file(self, global_settings):
        desktop_session = GLib.getenv ("DESKTOP_SESSION")
        path = ( "/etc/xdg" if global_settings else GLib.get_user_config_dir()) + '/lxsession/' + desktop_session + "/desktop.conf"
        return path
    
    
# ---------------------------------------------------------------------------------------    
    def get_lxpanel_file(self, global_settings):
        desktop_session = GLib.getenv ("DESKTOP_SESSION")
        path = ( "/etc/xdg" if global_settings else GLib.get_user_config_dir()) + '/lxpanel/' + desktop_session + "/panels/panel"
        return path        
    # ---------------------------------------------------------------------------------------    
    def get_pcmanfm_g_file(self, global_settings):
        desktop_session = GLib.getenv ("DESKTOP_SESSION")
        path = ( "/etc/xdg" if global_settings else GLib.get_user_config_dir()) + "/pcmanfm/" + desktop_session + "/pcmanfm.conf"
        return path
    
# ---------------------------------------------------------------------------------------        
    def get_libfm_file(self):
        desktop_session = GLib.getenv ("DESKTOP_SESSION")
        path = GLib.get_user_config_dir() + "/libfm/libfm.conf"
        return path