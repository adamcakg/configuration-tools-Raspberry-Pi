
import settings.main as main

class Controller:
    def __init__(self, window):
        self.window = window
        self.state = None
        self.set_state(main.Main())

    def set_state(self, s):
        if self.state is not None:
            self.window.remove(self.state.get_xml_object())
            self.state.destroy()

        self.state = s
        self.state.connect_handler(self)
        self.window.add(self.state.get_xml_object())
        self.window.show_all()

    def next(self):
        self.state.next(self)

    def back(self):
        self.state.back(self)

    def quit(self):
        self.window.close()
        exit(0)
