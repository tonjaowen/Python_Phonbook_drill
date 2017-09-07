# Python version: 3.5.1
#
# Purpose: Phonebook Demo.
#
# Author: Tonja Carney

#importing tkinter library

from tkinter import *
import tkinter as tk


import phonebook_gui
import phonebook_func


#defining the class.

class ParentWindow(Frame):

    def __init__(self, master, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)

        #defining the outer frame.
        self.master = master
        self.master.minsize(500,300)
        self.master.maxsize(500,300)

        #centering the app
        phonebook_func.center_window(self, 500,300)

        self.master.title("Tkinter Phonebook")
        self.master.configure(bg = "#F0F0F0")

        #capturing the windows close button feature
        self.master.protocol("WM_DELETE_WINDOW", lambda: phonebook_func.ask_quit(self))
        

        #loading GUI widgets
        phonebook_gui.load_gui(self)



def main():
    root = tk.Tk()
    App = ParentWindow(root)
    root.mainloop()



if __name__ == '__main__': main()


