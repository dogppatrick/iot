from Tkinter import *
from ttk import *
win=Tk()
win.title("ttk GUI")
label=Label(win, text="Hello World!")
count=0
def clickOK():
    global count
    count=count + 1
    label.config(text="Click OK " + str(count) + " times")

button=Button(win, text="OK", command=clickOK)
label.pack()
button.pack()
win.mainloop()
