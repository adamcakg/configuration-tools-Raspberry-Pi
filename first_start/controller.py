from page import Page
from handler import Handler
from list_of_pages import pages_dict
from list_of_pages import pages_dict_reversed


class Controller:
    def __init__(self, window):
        self.window = window                                                    # Storing window object
        self.state = None
        self.set_first_page()                                                   # Setting first page to Welcome screen

    def set_first_page(self):                                                   # Setting first page
        page = Page('welcome')                                                  # Creating welcome page
        self.state = page
        self.state.connect_to(Handler(self, self.state.get_state()))
        self.window.add(page.get_xml_object())

    def next_page(self):
        temp = pages_dict[self.state.get_state()]
        temp = pages_dict_reversed[temp+1]
        self.make_new_page(temp)

    def prev_page(self):
        temp = pages_dict[self.state.get_state()]
        temp = pages_dict_reversed[temp - 1]
        self.make_new_page(temp)

    def make_new_page(self, new_page):
        self.window.remove(self.state.get_xml_object())
        self.state.destroy()
        self.state = Page(new_page)

        self.state.connect_to(Handler(self, self.state.get_state()))
        self.window.add(self.state.get_xml_object())
        self.window.show_all()
