import random
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import GLib


class Welcomes:
    def __init__(self, welcome_label, window_label):
        self.__window_label = window_label

        self.__list_of_welcomes = ['Welcome', 'Vitajte', 'Willkommen', 'Bienvenidos', '어서 오세요', 'Bienvenue', 'أهلا بك']
        self.__label = welcome_label
        self.__previous = 'Welcome'
        GLib.timeout_add_seconds(5, self.get_random_welcome_text)

    def get_random_welcome_text(self):
        label = random.choice(self.__list_of_welcomes)

        while label == self.__previous:
            label = random.choice(self.__list_of_welcomes)

        self.__previous = label
        self.__label.set_label(label)
        self.__window_label.set_title(label)

        GLib.timeout_add_seconds(5, self.get_random_welcome_text)




