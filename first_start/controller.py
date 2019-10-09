from page import Page
from handler import Handler
from list_of_pages import pages_dict
from list_of_pages import pages_dict_reversed

# from list_of_welcomes import Welcomes


class Controller:
    def __init__(self, window):
        self.handler = Handler(self)
        self.window = window                                                    # Storing window object
        self.page = None
        self.set_first_page()                                                   # Setting first page to Welcome screen
        # self.welcomes = None

    def set_first_page(self):                                                   # Setting first page
        self.page = Page('welcome')                                             # Creating welcome page
        self.page.connect_to(Handler(self, self.page.get_state()))
        self.window.add(self.page.get_xml_object())
        # self.welcomes = Welcomes(self.page.get_builder().get_object("welcome_label"))

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
        # if self.welcomes:
        #     self.welcomes.destroy()
        self.window.remove(self.page.get_xml_object())
        self.page.destroy()
        self.page = Page(new_page)

        # if new_page == 'welcome':
        #     self.welcomes = Welcomes(self.page.get_builder().get_object("welcome_label"))


        self.page.connect_to(Handler(self, self.page.get_state()))
        self.window.add(self.page.get_xml_object())
