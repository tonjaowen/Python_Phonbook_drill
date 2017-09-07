import os
from tkinter import *
from tkinter import messagebox
import tkinter as tk
import sqlite3


import phonebook_main
import phonebook_gui


def center_window(self, w, h):

    #Center of the screen function
    screen_width = self.master.winfo_screenwidth()
    screen_height = self.master.winfo_screenheight()

    x = int((screen_width/2) - (w/2))
    y = int((screen_height/2) - (h/2))

    centerGeo = self.master.geometry('{}x{}+{}+{}'.format(w, h, x, y))
    return centerGeo

def ask_quit(self):
    if messagebox.askokcancel("Exit program", "Okay to exit application"):
        # close app
        self.master.destroy
        os._exit(0)


def create_db(self):
    conn = sqlite3.connect('phonebook.db')
    with conn:
        cur = conn.cursor()
        cur.execute("CREATE TABLE if not exists tbl_phonebook( \
                    ID INTEGER PRIMARY KEY AUTOINCREMENT, \
                    col_fname TEXT, \
                    col_lname TEXT, \
                    col_fullname TEXT, \
                    col_phone TEXT, \
                    col_email TEXT \
                    );")

        conn.commit()
    conn.close()
    first_run(self)


def first_run(self):

    data = ('John', 'Doe', 'John Doe', '111-111-1111', 'jdoe@gmail.com')
    conn = sqlite3.connect('phonebook.db')
    with conn:
        cur = conn.cursor()
        cur, count = count_records(cur)
        if count < 1:
            cur.execute("""INSERT INTO tbl_phonebook (col_fname,col_lname, col_fullname, col_phone, col_email) VALUES(?,?,?,?,?)""", (data[0], data[1], data[2], data[3], data[4]))
            conn.commit()
    conn.close()



def count_records(cur):
    count = ""
    cur.execute("""SELECT COUNT(*) FROM tbl_phonebook""")
    count = cur.fetchone()[0]
    return cur, count


#Selecting items from the list box

def onSelect(self, event):

    varList = event.widget
    select = varList.curselection()[0]
    value = varList.get(select)
    conn = sqlite3.connect('phonebook.db')
    with conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT col_fname, col_lname, col_phone, col_email FROM tbl_phonebook WHERE col_fullname = (?)""", [value])
        varBody = cursor.fetchall()

        for data in varBody:
            self.txt_fname.delete(0, END)
            self.txt_fname.insert(0, data[0])
            self.txt_lname.delete(0, END)
            self.txt_lname.insert(0, data[1])
            self.txt_phone.delete(0, END)
            self.txt_phone.insert(0, data[2])
            self.txt_email.delete(0, END)
            self.txt_email.insert(0, data[3])




def addToList(self):
    var_fname = self.txt_fname.get()
    var_lname = self.txt_lname.get()

    var_fname = var_fname.strip()
    var_lname = var_lname.strip()
    var_fname = var_fname.title()
    var_lname = var_lname.title()

    var_fullname = ("{} {}".format(var_fname, var_lname))

    var_phone = self.txt_phone.get().strip()
    var_email = self.txt_email.get().strip()

    if not '@' or not '.' in var_email:
        print("incorrect email")

    if(len(var_fname) > 0) and (len(var_lname) > 0) and (len(var_phone) > 0) and (len(var_email) > 0):
        conn = sqlite3.connect('phonebook.db')
        with conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT COUNT(col_fullname) FROM tbl_phonebook WHERE col_fullname = '{}'""".format(var_fullname))
            count = cursor.fetchone()[0]
            chkName = count
            if chkName == 0:
                print("chkName: {}".format(chkName))
                cursor.execute("""INSERT INTO tbl_phonebook(col_fname, col_lname, col_fullname, col_phone, col_email) VALUES (?,?,?,?,?)""",(var_fname,
                                                                                                                                                   var_lname, var_fullname,
                                                                                                                                                   var_phone, var_email))
                self.lst_list.insert(END, var_fullname) #updating the list box
                onClear(self)
            else:

                messagebox.showerror("Name Error", "'{}' already exists in the database! Please choose different name.".format(var_fullname))
                onClear(self)
    else:
        messagebox.showerror("Missing Text Error", "Please ensure that ther is data in all four fields.")
                               
                               
    
def onDelete(self):
    var_select = self.lst_list.get(self.lst_list.curselection()) #getting the list box's selection.
    conn = sqlite3.connect('phonebook.db')

    with conn:
        cur = conn.cursor()
        # checking to see if the last one.
        cur.execute("""SELECT COUNT(*) FROM tbl_phonebook""")
        count = cur.fetchone()[0]
        if count > 1:
            confirm = messagebox.askokcancel("Delete Confirmation", "Contact info of {} \n will be deleted".format(var_select))
            if confirm:
                conn = sqlite3.connect('phonebook.db')
                with conn:
                    cursor = conn.cursor()
                    cursor.execute("""DELETE FROM tbl_phonebook WHERE col_fullname = '{}'""".format(var_select))

                    onDeleted(self) # clearing the input boxes.

                    conn.commit()

        else:
            confirm = messagebox.showerror("Last Record Error", "Last record can not be deleted")
    conn.close()


def onDeleted(self):
    # clearing the text boxes
    self.txt_fname.delete(0, END)
    self.txt_lname.delete(0, END)
    self.txt_phone.delete(0, END)
    self.txt_email.delete(0, END)

    try:
        index = self.lst_list.curselection()[0]
        self.lst_list.delete(index)
    except IndexError:
        pass


def onClear(self):
                                             
    self.txt_fname.delete(0, END)
    self.txt_lname.delete(0, END)
    self.txt_phone.delete(0, END)
    self.txt_email.delete(0, END)

    
def onRefresh(self):
    # Populating the list box.
    self.lst_list.delete(0, END)
    conn = sqlite3.connect('phonebook.db')
    with conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT COUNT(*) FROM tbl_phonebook""")
        count = cursor.fetchone()[0]
        i = 0
        while i < count:
                cursor.execute("""SELECT col_fullname FROM tbl_phonebook""")
                varList = cursor.fetchall()[i]
                for item in varList:
                    self.lst_list.insert(0, str(item))
                    i = i + 1

    conn.close()



def onUpdate(self):
    try:
        var_select = self.lst_list.curselection()[0]
        var_value = self.lst_list.get(var_select)
    except:
        messagebox.showinfo("Missing selection", "No name was selected")
        return

    # User is only allowed to delete phone and email info.
    var_phone = self.txt_phone.get().strip()
    var_email = self.txt_email.get().strip()

    if (len(var_phone) > 0) and (len(var_email) > 0):
        conn = sqlite3.connect('phonebook.db')
        with conn:
            cur = conn.cursor()
            # checking to see is record is already exists
            cur.execute("""SELECT COUNT(col_phone) FROM tbl_phonebook WHERE col_phone = '{}'""".format(var_phone))
            count = cur.fetchone()[0]
            print(count)
            cur.execute("""SELECT COUNT(col_email) FROM tbl_phonebook WHERE col_email = '{}'""".format(var_email))
            count2 = cur.fetchone()[0]
            print(count2)

            if count == 0 or count == 0:
                response = messagebox.askokcancel("Update Request", "Record will be implemented")
                print(response)
                if response:
                    with conn:
                        cursor = conn.cursor()
                        cursor.execute("""UPDATE tbl_phonebook SET col_phone = '{}', col_email = '{}' WHERE col_fullname = '{}'""".format(var_phone, var_email, var_value))
                        onClear(self)
                        conn.commit()
                else:
                    messagebox.showinfo("Cancel Request", "No changes has been made to {}.".format(var_value))
        
            else:
                messagebox.showinfo("No Changes detected", "Record already exists")
            onClear(self)
        conn.close()

    else:
        messagebox.showerror("Missing Information", "Please select a name from the list to update")

    onClear(self)

if __name__ == "__main__":
    pass









