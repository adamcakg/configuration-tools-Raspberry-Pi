from keeper import keeper

import os


class Handler:
    def __init__(self,builder):
                         # handling instance of controller
        self.builder = builder
        self.can_go_on = False                          # variable that keeping state if i can move on on next page
        self.confirmed = keeper['passwordpage'][ 'password']            # getting password from keeper
    
    def add_controller(self, controller):
        self.controller = controller
# NEXT
# ----------------------------------------------------------------------------------------------------------------------
    def next(self, button):
        password = self.builder.get_object('password').get_text()
        confirmed = self.builder.get_object('confirmed').get_text()
        
        if password == '':
            self.builder.get_object('password_label').set_opacity(0) 
            self.builder.get_object('missing_password_label').set_opacity(1) 
        elif self.compare(password, confirmed):  # checking if passwords are the same
            keeper['passwordpage']['password'] = password
            self.controller.execute()                       # executing page settings
        else:
            self.builder.get_object('missing_password_label').set_opacity(0) 
            self.builder.get_object('password_label').set_opacity(1) 
# BACK
# ----------------------------------------------------------------------------------------------------------------------
    def back(self, button):
        keeper['passwordpage']['password'] = self.builder.get_object('password').get_text()
        self.controller.back()                              # moving to previous page
        
# METHOD TO HANDLE ENTRY WITH PASSWORD
# ----------------------------------------------------------------------------------------------------------------------
    def input_password(self, entry, text, length, position):
        self.check_strength_of_password(self.builder.get_object('password').get_text())

# METHOD TO HANDLE ENTRY WITH PASSWORD WHEN DELETING
# ----------------------------------------------------------------------------------------------------------------------
    def input_password_back(self, entry):
        self.check_strength_of_password(self.builder.get_object('password').get_text())

# METHOD TO COMPARE PASSWORDS(STRINGS)
# ----------------------------------------------------------------------------------------------------------------------
    def compare(self, string1, string2):   # checking if strings are the same
        if string1 == '' or string2 == '':
            return False
        elif string1 == string2:
            return True
        else:
            return False

# METHOD TO CHECK AND SET STRENGTH OF PASSWORD
# ----------------------------------------------------------------------------------------------------------------------
    def check_strength_of_password(self, password):
        # strength is from 0 to 10
        special_chars = '!@#$%^&*()_+-={}[];:\\\"\'/?.>,<`~§±'
        strength = 0
        is_number = False
        is_upper = False
        is_special = False

        if len(password) > 5:
            strength += 2

        if len(password) > 10:
            strength += 2

        for i in password:
            if i.isupper():
                is_upper = True
            if i.isnumeric():
                is_number = True
            if i in special_chars:
                is_special = True

        if is_number:
            strength += 2
        if is_upper:
            strength += 2
        if is_special:
            strength += 2

        self.builder.get_object('level_bar').set_value(strength)
        
# THREAD FUNCTION
# ---------------------------------------------------------------------------------------------------
    def thread_function(self):
        password = keeper['passwordpage']['password'] + '\n' + keeper['passwordpage']['password']
        os.system('echo "{}" | sudo passwd "pi"'.format(password))
        
    def create_modal(self):
        print('modal function')
        dialog = self.builder.get_object('password_dialog')
        dialog.set_attached_to(self.builder.get_object('settings'))
        dialog.set_destroy_with_parent(True)
        dialog.set_modal(True)
        dialog.show_all()
        print('modal displayed')
        
    def delete_modal(self):
        dialog = self.builder.get_object('password_dialog')
        dialog.destroy()
        self.controller.next()
        
    
