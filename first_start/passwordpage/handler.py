from test.keeper import update_keeper
from test.keeper import get_atribute_from_keeper


class Handler:
    def __init__(self, controller):
        self.controller = controller
        self.can_go_on = False
        self.confirmed = get_atribute_from_keeper('passwordpage', 'password')

    def next(self, button):
        if self.compare(get_atribute_from_keeper('passwordpage', 'password'), self.confirmed):
            self.controller.next()

    def back(self, button):
        if self.compare(get_atribute_from_keeper('passwordpage', 'password'), self.confirmed):
            self.controller.back()

    def input_password(self, entry, text, length, position):
        password = get_atribute_from_keeper('passwordpage', 'password') + text
        update_keeper('passwordpage', 'password', password)

    def input_password_back(self, entry):
        password = get_atribute_from_keeper('passwordpage', 'password')[:-1]
        update_keeper('passwordpage', 'password', password)

    def input_confirm_password(self, entry, text, length, position):
        self.confirmed += text

    def input_confirm_password_back(self, entry):
        self.confirmed = self.confirmed[:-1]

    @staticmethod
    def compare(string1, string2):
        if string1 == '' or string2 == '':
            return False
        elif string1 == string2:
            return True
        else:
            return False



