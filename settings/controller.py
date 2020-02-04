
import main
from header import Header
from main import Main

class Controller:
    def __init__(self, window):
        self.window = window
        self.state = None
        self.header = Header()
        self.set_title_bar(self.header)
        self.main = Main()
        self.set_left_bar(self.main)
        
    def set_title_bar(self, header):
        self.window.set_titlebar(header.get_xml_object())
        header.connect_handler(self)
        
    def set_left_bar(self, main):
        self.window.add(main.get_xml_object())
        main.connect_handler(self)

    def set_state(self, new_state):
        print(new_state)

        box = self.main.get_xml_object()
        
        if self.state is not None:
            box.remove(self.state.get_xml_object())
            self.state.destroy()

        self.state = new_state
        self.state.connect_handler(self)
        self.state.connect_header(self.header)
        box.add(self.state.get_xml_object())
        self.window.show_all()

    def quit(self):
        self.window.close()
        exit(0)
