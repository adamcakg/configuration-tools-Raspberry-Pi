

from wifi import Wifi
from bluetooth import Bluetooth
from appearance import Appearance


def get_pages():
        """
        Here are the pages of all application
        ['name', Instance]
        :return - list of pages with instances
        """
        return [
            ['WiFi', Wifi()],
            ['Bluetooth', Bluetooth()],
            ["Appearance", Appearance()]

        ]