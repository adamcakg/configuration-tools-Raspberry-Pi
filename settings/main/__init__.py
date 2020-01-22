import gi
from .handler import Handler
from wifi import Wifi
from bluetooth import Bluetooth

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Main:
    def __init__(self):
        self.__builder = Gtk.Builder()                  # Initializing builder
        self.__builder.add_from_file('main/main.glade')   # creating object from XML(.glade files)
        
        self.handler = Handler(builder=self.__builder)
        self.pages = None

    def get_xml_object(self):
        return self.__builder.get_object('main')

    def destroy(self):
        del self

    def connect_handler(self, controller):
        self.handler.add_controller(controller)
        self.__builder.connect_signals(self.handler)
        
    def set_pages(self):
        self.pages = self.get_pages()
        self.handler.add_pages(self.pages)
        
        list_box = self.__builder.get_object("main_list_box")
        list_box.connect("row-selected", self.handler.row_activated)
        
        for page in self.pages:
            list_box.insert(Gtk.Label.new(page[0]),-1)
        
    def get_pages(self):
        """
        Here are the pages
        ['name', Instance]
        """
        return [
            ['WiFi', Wifi()],
            ['Bluetooth', Bluetooth()]
            
            
            
            
            
            
            ]
        
        
        
        
        
        
        
        
        
        
