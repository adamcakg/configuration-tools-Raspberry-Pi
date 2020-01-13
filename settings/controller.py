
import main
from header import Header
from main import Main

class Controller:
    def __init__(self, window):
        self.window = window
        self.state = None
        self.header = Header()
        self.set_title_bar(self.header)
        self.set_state(Main())
        
    def set_title_bar(self, header):
        self.window.set_titlebar(header.get_xml_object())
        header.connect_handler(self)

    def set_state(self, s):
        if self.state is not None:
            self.window.remove(self.state.get_xml_object())
            self.state.destroy()

        self.state = s
        self.state.connect_handler(self)
        self.state.connect_header(self.header)
        self.window.add(self.state.get_xml_object())
        self.window.show_all()
        
    def get_state(self):
        return self.state

    def next(self):
        self.state.next(self)

    def back(self):
        self.state.back(self)

    def quit(self):
        self.window.close()
        exit(0)
