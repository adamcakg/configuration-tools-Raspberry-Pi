
from info import Info
from wifi import Wifi
from bluetooth import Bluetooth
from appearance import Appearance
from system import System
from localisation import Localisation
from interfaces import Interfaces
from accessibility import Accessibility
from display import Display

def get_pages():
        """
        Here are the pages of all application
        [instance]
        :return - list of pages with instances
        """
        return [
            System(),
            Appearance(),
            Accessibility(),
            Interfaces(),
            Display(),
            Localisation(),
            Info(),
            Wifi(),
            Bluetooth()
        ]