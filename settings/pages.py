

from wifi import Wifi
from bluetooth import Bluetooth
from appearance import Appearance
from system import System
from localisation import Localisation
from interfaces import Interfaces
from accessibility import Accessibility

def get_pages():
        """
        Here are the pages of all application
        ['name', Instance]
        :return - list of pages with instances
        """
        return [
            System(),
            Accessibility(),
            Appearance(),
            Localisation(),
            Wifi(),
            Bluetooth(),
            Interfaces()
            
        ]