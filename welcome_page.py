import tkinter
from page import Page


class WelcomePage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        tkinter.Label(self, text="WELCOME", font=("Courier", 44)).place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        tkinter.Button(self, text="Enter", command=self._next_page).place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)

        self.next = None

    def set_next(self, next_page):
        self.next = next_page

    def _next_page(self):
        self.next.lift()
