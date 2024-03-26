import tkinter
from tkinter import Frame, Label, Scrollbar, Canvas, OUTSIDE, VERTICAL,HORIZONTAL, BOTH, BOTTOM,TOP, FALSE, TRUE, N, RIGHT, LEFT, X, Y, W, E

canvasW=600;canvasD=500
canvas:Canvas=None
i=0
def zoomButtonAction( event):
    global i;global canvas
    canvas.config(scrollregion=(0,0,canvas.winfo_width()+800,canvas.winfo_depth()+800))
    #print ("new width",canvas.winfo_width())

def showCursorCoordinates( event):
    xyLabel.config(text = "x="+str(round((event.x),2))+" y="+" Ty="+str(round((event.y),2)))
    
def draw():
    global canvas
    canvas.create_rectangle(1, 1, canvasW-2, canvasD-2, fill="orange")

def createCanvas(parentFrame)->Canvas:
    global canvas
    canvas = Canvas(parentFrame, width=canvasW, height= canvasD, bd=0,bg="red", cursor="crosshair",highlightthickness=0, highlightbackground="white")
    sbHorizontalScrollBar = Scrollbar(parentFrame)
    sbVerticalScrollBar = Scrollbar(parentFrame)
    # Sets up the Canvas, Frame, and scrollbars for scrolling
    canvas.config(xscrollcommand=sbHorizontalScrollBar.set,yscrollcommand=sbVerticalScrollBar.set, highlightthickness=0)
    sbHorizontalScrollBar.config(orient=HORIZONTAL, command=canvas.xview)
    sbVerticalScrollBar.config(orient=VERTICAL, command=canvas.yview)
    sbHorizontalScrollBar.pack(fill=X, side=BOTTOM, expand=FALSE)
    sbVerticalScrollBar.pack(fill=Y, side=RIGHT, expand=FALSE)
    canvas.pack_configure(fill=BOTH, anchor="center", side=LEFT, expand=TRUE)
    # scrollbarWidth=sbVerticalScrollBar.winfo_depth()
    canvas.update_idletasks()
    #canvas.config(scrollregion=(0,0,canvasW+500,canvasD+1000))
    draw()
    print ("initial width", canvasW)
    canvas.bind("<Button-1>", zoomButtonAction)  
    canvas.bind("<Motion>", showCursorCoordinates)
    return canvas, 32 # todo returnthe measured value

# really here is where the UI starts being built
rootWindow = tkinter.Tk()
spreadOnX=.95;spreadOnY=.8
rootWindow.geometry(str(int(rootWindow.winfo_screenwidth()*spreadOnX))+"x"+str( int(rootWindow.winfo_screenheight()*spreadOnY))+
                                                                         "+"+str( int(rootWindow.winfo_screenwidth()*(1-spreadOnX)/2))+
                                                                         "+"+str( int(rootWindow.winfo_screenheight()*(1-spreadOnY)/2)))
rootWindow.configure(background='blue') 
frameLabelHolder = Frame(rootWindow, bg= "green")
frameLabelHolder.place_configure(relwidth=0.5, relheight=1, relx=.5, bordermode =OUTSIDE)        
frameCanvasAndScrollBarsHolder = Frame(rootWindow, bg= "yellow")
frameCanvasAndScrollBarsHolder.place_configure(relwidth=0.5, relheight=1, relx=0, bordermode =OUTSIDE)       
xyLabel = Label(frameLabelHolder, text = "Coordinates")
xyLabel.place_configure(relwidth=0.5, relheight=.05, rely=0,  relx=0, bordermode =OUTSIDE)   
# xyLabel.grid(row=0, column=0)             
elementNameLabel:Label = Label(frameLabelHolder, text = "Element Name")
elementNameLabel.place_configure(relwidth=0.5, relheight=.05, relx=0, rely=.05, bordermode =OUTSIDE)
canvas, scrollBarWidth=createCanvas(frameCanvasAndScrollBarsHolder) 
firstDraw=False # so we don't over collect screenElements
rootWindow.mainloop()# based on https://www.joehutch.com/posts/tkinter-dynamic-scroll-area/


