import gi
from pages import get_pages


gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Handler:
    def __init__(self, builder):
        self.builder = builder
        self.pages = None
        self.set_pages()
        self.controller = None
        
# ADDING CONTROLLER TO HANDLER
# ----------------------------------------------------------------------------------------------------------------------        
    def add_controller(self, controller):
        self.controller = controller

    def row_activated(self, list_box, list_row):
        page_index = list_row.get_index()
        page = get_pages()[page_index][1]
        self.next_page(page)
        
    def next_page(self, next_page):
        self.controller.set_state(next_page)

    def set_pages(self):
        pages = get_pages()

        list_box = self.builder.get_object("main_list_box")
        list_box.connect("row-selected", self.row_activated)

        for page in pages:
            list_box.insert(Gtk.Label.new(page[0]), -1)

