import tkinter
from page import Page


class NamePage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        tkinter.Label(self, text="PAGE 2", font=("Courier", 44)).place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

        tkinter.Entry(self).place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        tkinter.Button(self, text="Next", command=self._next_page).place(relx=0.9, rely=0.9, anchor=tkinter.CENTER)
        tkinter.Button(self, text="Back", command=self._previous_page).place(relx=0.1, rely=0.9, anchor=tkinter.CENTER)

        self.next = None
        self.previous = None

    def set_next_and_previous(self, next_page, previous_page):
        self.next = next_page
        self.previous = previous_page

    def _next_page(self):
        self.next.lift()

    def _previous_page(self):
        self.previous.lift()
