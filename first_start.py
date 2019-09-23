import tkinter


class Page(tkinter.Frame):
    def __init__(self, *args, **kwargs):
        tkinter.Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()


class Page1(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        lbl_welcome = tkinter.Label(self, text="WELCOME", font=("Courier", 44)).place(relx=0.5, rely=0.5,
                                                                                                anchor=tkinter.CENTER)


class Page2(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        lbl_pg_2 = tkinter.Label(self, text="PAGE 2", font=("Courier", 44)).place(relx=0.5, rely=0.5,
                                                                                                anchor=tkinter.CENTER)


class Page3(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        lbl_pg_3 = tkinter.Label(self, text="PAGE 3", font=("Courier", 44)).place(relx=0.5, rely=0.5,
                                                                                  anchor=tkinter.CENTER)


class MainView(tkinter.Frame):
    def __init__(self, *args, **kwargs):
        tkinter.Frame.__init__(self, *args, **kwargs)
        p1 = Page1(self)
        p2 = Page2(self)
        p3 = Page3(self)

        progress_frame = tkinter.Frame(self)
        button_frame = tkinter.Frame(self)
        container = tkinter.Frame(self)
        progress_frame.pack(side='top', fill='x', expand=False)
        button_frame.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = tkinter.Button(button_frame, text="Page 1", command=p1.lift)
        b2 = tkinter.Button(button_frame, text="Page 2", command=p2.lift)
        b3 = tkinter.Button(button_frame, text="Page 3", command=p3.lift)

        b1.pack(side="left")
        b2.pack(side="left")
        b3.pack(side="left")

        p1.show()


if __name__ == "__main__":
    root = tkinter.Tk()
    root.title("Raspberry PI")
    # root.attributes('-fullscreen', True)
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("400x400")
    root.mainloop()



# lbl_welcome = tkinter.Label(window, text="WELCOME", font=("Courier", 44)).place(relx=0.5, rely=0.5,
#                                                                                 anchor=tkinter.CENTER)
# lbl_welcome_enter = tkinter.Button(window, text="Enter", command= window.quit).place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)
