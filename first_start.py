import tkinter
from welcome_page import WelcomePage
from name_page import NamePage
from password_page import PasswordPage
from all_set import AllSetPage


class MainView(tkinter.Frame):
    def __init__(self, *args, **kwargs):
        tkinter.Frame.__init__(self, *args, **kwargs)

        p1, p2, p3, p4 = WelcomePage(self), NamePage(self), PasswordPage(self), AllSetPage(self)

        p1.set_next(p2)
        p2.set_next_and_previous(p3, p1)
        p3.set_next_and_previous(p4, p2)

        progress_frame = tkinter.Frame(self)
        button_frame = tkinter.Frame(self)
        container = tkinter.Frame(self)
        progress_frame.pack(side='top', fill='x', expand=False)
        button_frame.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p4.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = tkinter.Button(button_frame, text="Page 1", command=p1.lift)
        b2 = tkinter.Button(button_frame, text="Page 2", command=p2.lift)
        b3 = tkinter.Button(button_frame, text="Page 3", command=p3.lift)
        b4 = tkinter.Button(button_frame, text="Page 3", command=p4.lift)

        b1.pack(side="left")
        b2.pack(side="left")
        b3.pack(side="left")
        b4.pack(side="left")

        p1.show()


if __name__ == "__main__":
    root = tkinter.Tk()
    root.title("Raspberry PI")
    root.attributes('-fullscreen', True)
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("400x400")
    root.mainloop()

