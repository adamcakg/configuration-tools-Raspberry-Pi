import random
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import GLib


class Welcomes:
    def __init__(self, welcome_label):
        print('welcomes class was created')

        self.__list_of_welcomes = ['Welcome', 'Vitajte', 'Willkommen', 'Bienvenidos', '어서 오세요', 'Bienvenue', 'أهلا بك']
        self.__label = welcome_label
        self.__previous = 'Welcome'
        GLib.timeout_add_seconds(5, self.__get_random_welcome_text)

    def __get_random_welcome_text(self):
        label = random.choice(self.__list_of_welcomes)

        while label == self.__previous:
            label = random.choice(self.__list_of_welcomes)

        self.__previous = label
        self.__label.set_label(label)

        GLib.timeout_add_seconds(5, self.__get_random_welcome_text)

    def destroy(self):
        print("welcomes class was destroyed")
        del self





