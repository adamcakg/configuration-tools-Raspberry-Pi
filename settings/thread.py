import time

import threading


class Thread(object):
    def __init__(self, handler):
        self.handler = handler
        self.thread = threading.Thread(target=self.run, args=())
        self.thread.daemon = True
        self.thread.start()

    def run(self):
        self.handler.thread_function()

    def alive(self):
        return self.thread.is_alive()