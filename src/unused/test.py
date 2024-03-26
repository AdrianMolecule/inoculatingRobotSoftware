from tkinter import *
  
class ScrollBar:
     
    # constructor
    def __init__(self):
         
        # create root window
        root = Tk()
  
        # create a horizontal scrollbar by
        # setting orient to horizontal
        h = Scrollbar(root, orient = 'horizontal')
  
        # attach Scrollbar to root window at 
        # the bootom
        h.pack(side = BOTTOM, fill = X)
  
        # create a vertical scrollbar-no need
        # to write orient as it is by
        # default vertical
        v = Scrollbar(root)
  
        # attach Scrollbar to root window on 
        # the side
        v.pack(side = RIGHT, fill = Y)
        f=Frame(root, width=4000, height= 6000,xscrollcommand = h.set,    yscrollcommand = v.set)
        self.canvas = Canvas(f, width=4000, height= 6000, bd=0,bg="white", cursor="crosshair",
                              highlightthickness=0, highlightbackground="blue")
        f.pack(side=TOP, fill=X)
        # here command represents the method to
        # be executed xview is executed on
        # object 't' Here t may represent any
        # widget
        h.config(command=f.xview)
        # here command represents the method to
        # be executed yview is executed on
        # object 't' Here t may represent any
        # widget
        v.config(command=f.yview)
        for drop in range(1,1000):
            self.canvas.create_oval(drop+1, drop+1, drop+100, drop+100, fill="green")

        # the root window handles the mouse
        # click event
        root.mainloop()
 
# create an object to Scrollbar class
s = ScrollBar()