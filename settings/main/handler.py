
from wifi import Wifi
from bluetooth import Bluetooth

class Handler:
    def __init__(self, builder):
        self.builder = builder
        self.pages = None
        
# ADDING CONTROLLER TO HANDLER
# ----------------------------------------------------------------------------------------------------------------------        
    def add_controller(self, controller):
        self.controller = controller

    def row_activated(self, list_box, list_row):
        page_index = list_row.get_index()
        page = self.pages[page_index][1]
        self.next_page(page)
        
    def next_page(self, next_page):
        self.controller.set_state(next_page)
        
    
    def add_pages(self, pages):
        self.pages = pages