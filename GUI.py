from multiprocessing.connection import wait
import tkinter as tk
from tkinter import Canvas, Entry, Event, Frame, Label, Toplevel, Widget, ttk , Button
from tkinter.constants import ANCHOR, END, LEFT, NSEW
from typing import Text
from pandas.core.window.rolling import Window
import tkintertable as tktable
from tkintertable import TableCanvas , TableModel


#dummy data
import numpy as np
db = np.zeros((10,5))

#tkinter screen
root = tk.Tk()
screen = root.maxsize()

root.geometry(f"{screen[0]}x{screen[1]}")
root.title("Accounting Books")


#radio box
customer_radio = ttk.Radiobutton(root, text="Customer" , value='Customer').grid(column=0 , row=10,padx=0,pady=15)
supplier_radio = ttk.Radiobutton(root, text="Supplier" , value='Supplier').grid(column=1 , row=10,padx=0,pady=15)


#List box
ttk.Label(root, text = "Select Ledger:", 
        font = ("Times New Roman", 10)).grid(column=0,row=12,padx=0, pady = 25)

n = tk.StringVar()
Ledger =ttk.Combobox(root , width=27 , textvariable= n)
Ledger.grid(column=1 , row=12 , padx=0 , pady=25)


#spreadsheet tree
tree  = ttk.Treeview(root , columns= ("S#" , "Name" , "Rate" , "Qty" , "Total") , show="headings")

tree.heading("S#" , text="S#")
tree.heading("Name" , text="Name")
tree.heading("Rate" , text="Rate")
tree.heading("Qty" , text="Qty")
tree.heading("Total" , text="Total")

#dummy data
for i in range(1,10):
    if i%2 == 0:
        tree.insert('',tk.END,values=db[i] , tags=('odd',))
    else:
        tree.insert('',tk.END,values=db[i] , tags=('even',))
tree.tag_configure('odd',background='orange')

tree.grid(column=0,columnspan=30, row=16)

#global variable neccessary to hold value to edit
new_value = tk.StringVar()


def edit_window_box(val):
    
    edit_window = Toplevel(root)
    edit_window.title("Edit the value or cancel")
    edit_window.geometry("1000x250")
    label_edit = tk.Label(edit_window , text='Enter value to edit or press cancel', 
    font = ("Times New Roman", 10)).grid(column=0,row=1,padx=0, pady = 2)
    #create edit box
    edit_box = tk.Entry(edit_window)
    edit_box.insert(0,val)
    edit_box.grid(column=1,row=1,padx=0,pady=2)
    #auto select edit window 
    edit_window.focus()
    
    def value_assignment(event):
        printing = edit_box.get()
        new_value.set(printing)
        #only destroy will not update the value (perhaps event keeps running in background)
        #quit allows event to stop n update value in tree but does not close the window in single click 
        #rather on dbl click shuts down entire app 
        edit_window.quit()
        edit_window.destroy()
    
    edit_window.bind('<Return>', value_assignment )

    B1 = tk.Button(edit_window, text="Okay")
    B1.bind('<Button-1>',value_assignment)
    B1.grid(column=0,row=10,padx=0, pady = 20)
    
    B2 = tk.Button(edit_window, text="Cancel", command = edit_window.destroy).grid(column=1,row=10,padx=10, pady = 20)
    edit_window.mainloop()
    
#will explain
#variable to hold col value (col clicked)
shape1 = tk.IntVar()
#tracks both col , row on mouse click
def tree_click_handler(event):
    cur_item = tree.item(tree.focus())
    col = tree.identify_column(event.x)[1:]
    rowid = tree.identify_row(event.y)[1:]
    #updates list
    shape1.set(col)
    try:
        x,y,w,h = tree.bbox('I'+rowid,'#'+col)
    except:pass
    #tree.tag_configure("highlight", background="yellow")
    return(col)
    
#code linked to event    
tree.bind('<ButtonRelease-1>', tree_click_handler)




def delete_row():
    try:
        selected_item = tree.selection()[0]
        tree.delete(selected_item)
    except: pass



def delete_value():
    try:
        selected_item = tree.selection()[0]
        temp = list(tree.item(selected_item , 'values'))
        tree_click_handler
        col_selected = int(shape1.get())-1
        temp[col_selected]= ''
        
        tree.item(selected_item, values= temp)
    except: pass

#edit a value in a clicked cell
def edit(event):
    try:
        selected_item = tree.selection()[0]
        temp = list(tree.item(selected_item , 'values'))
        tree_click_handler
        col_selected = int(shape1.get())-1
        edit_window_box(temp[col_selected])
        #do not run if edit window is open
        #use edit_window.mainloop() so value assign after window closes
        temp[col_selected] = new_value.get()
        tree.item(selected_item, values= temp)
    except: pass
    
    
#binding allows to edit on screen double click
tree.bind('<Double-Button-1>' , edit)


style = ttk.Style()
'''# this is set background and foreground of the treeview
style.configure("Treeview",
                background="none",
                foreground="black",
                fieldbackground="green")'''

# set backgound and foreground color when selected
style.map('Treeview', background=[('selected', 'green')], foreground = [('focus','blue')])


#to call an event that rewuires handler via button also enter handler like tree_click_handler("<Escape>")
button_del = Button(root, text="Delete Row", command=delete_row)
button_del.grid(column=31,row=15)

button_del_cell = Button(root, text="Delete Cell", command=delete_value)
button_del_cell.grid(column=31,row=20)


root.mainloop()