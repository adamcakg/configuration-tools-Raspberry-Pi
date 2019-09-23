import tkinter
from page import Page


class AllSetPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        tkinter.Label(self, text="ALL SET", font=("Courier", 44)).place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        tkinter.Button(self, text="Start using PI", command=self.quit).place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)
