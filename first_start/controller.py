from page import Page
from handler import Handler
from list_of_pages import pages_dict
from list_of_pages import pages_dict_reversed


import gi

gi.require_version('Gtk', '3.0')

# from list_of_welcomes import Welcomes


class Controller:
    def __init__(self, window):
        self.handler = Handler(self)
        self.window = window                                                    # Storing window object
        self.page = None
        self.set_first_page()                                                   # Setting first page to Welcome screen

    def set_first_page(self):                                                   # Setting first page
        self.page = Page('welcome')                                             # Creating welcome page
        self.page.connect_to(self.handler)
        self.window.add(self.page.get_xml_object())

    def next_page(self):
        temp = pages_dict[self.page.get_state()]
        temp = pages_dict_reversed[temp+1]
        self.make_new_page(temp)
        self.window.show_all()

    def prev_page(self):
        temp = pages_dict[self.page.get_state()]
        temp = pages_dict_reversed[temp - 1]
        self.make_new_page(temp)
        self.window.show_all()

    def make_new_page(self, new_page):
        self.window.remove(self.page.get_xml_object())
        self.page.destroy()
        self.page = Page(new_page)

        self.page.connect_to(self.handler)
        self.window.add(self.page.get_xml_object())
