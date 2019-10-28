import test.welcome as welcome


class Controller:
    def __init__(self, window):
        self.window = window
        self.state = None
        self.set_state(welcome.WelcomePage())                                   # creating first state

    def set_state(self, s):
        if self.state is not None:
            self.window.remove(self.state.get_xml_object())                     # removing old object from window
            self.state.destroy()                                                # destroying current page

        self.state = s                                                          # setting new state
        self.state.connect_handler(self)                                        # connecting handler to page
        self.window.add(self.state.get_xml_object())                            # adding object to window
        self.window.show_all()                                                  # displaying on window

    def next(self):                                                             # moving to next state
        self.state.next(self)

    def back(self):                                                             # moving to previous state
        self.state.back(self)

    def execute(self):                                                          # executing page
        self.state.execute()

    def quit(self):                                                             # quiting window and code...
        self.window.close()
        exit(0)
