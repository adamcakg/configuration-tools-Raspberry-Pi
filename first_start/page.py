import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


# Default page
class Page:
    def __init__(self, page_name):

        self.__builder = Gtk.Builder()                                          # Initializing builder
        self.__builder.add_from_file('glade/{}.glade'.format(page_name))        # creating object from XML(.glade files)
        self.__name = page_name                                                 # Storing name of page

        print('Page created -> ' + self.__name)

    def get_xml_object(self):                                                   # Returning BOX object
        return self.__builder.get_object(self.__name)

    def connect_to(self, class_to_connect):                                     # Connecting handler into page class
        self.__builder.connect_signals(class_to_connect)

    def destroy(self):                                                          # Destroying itself
        print('Page destroyed -> ' + self.__name)
        del self

    def get_state(self):                                                        # Getting state (name)
        return self.__name
