from test.keeper import keeper


class Handler:
    def __init__(self, controller):
        self.controller = controller                    # handling instance of controller
        self.can_go_on = False                          # variable that keeping state if i can move on on next page
        self.confirmed = keeper['passwordpage'][ 'password']            # getting password from keeper

    def next(self, button):
        if self.compare(keeper['passwordpage']['password'], self.confirmed):  # checking if passwords
                                                                                                # are the same
            self.controller.execute()                       # executing page settings
            self.controller.next()                          # moving to next page

    def back(self, button):
        self.controller.back()                              # moving to previous page

    def input_password(self, entry, text, length, position):
        password = keeper['passwordpage']['password'] + text      # password + char
        keeper['passwordpage']['password'] = password                          # updating keeper

    def input_password_back(self, entry):
        password = keeper['passwordpage']['password'][:-1]        # len(password) - 1
        keeper['passwordpage']['password'] = password                         # updating keeper

    def input_confirm_password(self, entry, text, length, position):
        self.confirmed += text

    def input_confirm_password_back(self, entry):
        self.confirmed = self.confirmed[:-1]

    def compare(self, string1, string2):                                              # checking if strings are the same
        if string1 == '' or string2 == '':
            return False
        elif string1 == string2:
            return True
        else:
            return False



