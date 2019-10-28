from test.keeper import keeper


class Handler:
    def __init__(self, controller):
        self.controller = controller

    def next(self,button):
        self.controller.next()

    def back(self,button):
        self.controller.back()

    def country_handler(self, item):
        print('Country')
        keeper['settingspage']['country'] = item.get_active_text()

    def language_handler(self, item):
        print('language')
        keeper['settingspage']['language'] = item.get_active_text()

