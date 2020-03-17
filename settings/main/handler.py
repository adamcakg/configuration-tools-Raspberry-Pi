from pages import get_pages

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf

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
        page = get_pages()[page_index]
        self.next_page(page)
        
    def next_page(self, next_page):
        self.controller.set_state(next_page)

    def set_pages(self):
        pages = get_pages()

        list_box = self.builder.get_object("main_list_box")
        list_box.connect("row-selected", self.row_activated)

        for page in pages:
            box = Gtk.Box(spacing=0)
            try:
                icon = GdkPixbuf.Pixbuf.new_from_file_at_scale(filename= page.get_icon(),
                                                             width=8, height=8, 
                                                             preserve_aspect_ratio=True)
            except Exception:
                icon = GdkPixbuf.Pixbuf.new_from_file_at_scale(filename='main/img/minus.png',
                                                             width=8, height=8, 
                                                             preserve_aspect_ratio=True)
            icon = Gtk.Image.new_from_pixbuf(icon)
            box.pack_start(icon, False, False, 10)
            label = Gtk.Label.new(page.get_name())
            label.set_xalign(0)
            box.pack_start(label, False, False, 0)
                    
            list_box.insert(box, -1)
            #list_box.insert(Gtk.Label.new(page.get_name()), -1)

