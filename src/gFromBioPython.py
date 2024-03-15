from tkinter import *
from tkinter import filedialog
from collections import deque
from tkinter import messagebox
 

class Window:
    def __init__(self, master):
        self.master = master
        self.mainFrame = Frame(self.master)
        self.stack = deque(maxlen = 10)
        self.stackcursor = 0
        #LABEL
        self.sequenceLabel = Label(self.mainFrame, text = "Please load a Fasta File")
        self.sequenceLabel.pack(padx = 5, pady = 5)
        #ForbiddenList
        # Add a List Scrollbar(vertical)'
        # listScrollbar=Scrollbar(self.mainFrame, orient='vertical')
        # listScrollbar.pack(side = RIGHT, fill = BOTH)
        forbiddenItems=[]
        var = Variable(value=forbiddenItems)
        # self.forbiddenList = Listbox( self.mainFrame, listvariable=var, height=1, selectmode=EXTENDED )

        #listScrollbar.config(command = self.forbiddenList.yview)
         # Add a Scrollbar(horizontal)
        textScrollbar=Scrollbar(self.mainFrame, orient='horizontal')
        textScrollbar.pack(side=BOTTOM, fill='x')  
        self.sequenceTextBox:Text = Text(self.mainFrame, xscrollcommand=textScrollbar.set,wrap="none" )
        #self.sequenceText.insert(END, initialText)
        self.sequenceTextBox.edit
        #self.forbiddenList.pack(side= RIGHT, fill= BOTH)     
        self.sequenceTextBox.pack(padx = 5, pady = 5,fill= BOTH)
        textScrollbar.config(command=self.sequenceTextBox.xview)
        #text.pack()
        self.menu = Menu(self.mainFrame)
        #  self.menu.add_command(label = "Load Fasta", command = self.loadFastaFromFile)
        # self.menu.add_command(label = "Print", command = self.printStack)
        # self.menu.add_command(label = "Undo", command = self.undo)
        # self.menu.add_command(label = "Redo", command = self.redo)
        #self.menu.add_command(label = "Show Forbidden", command = self.showForbiddenListFromFile)
        #self.menu.add_command(label = "Load Forbidden Sites", command = self.loadForbiddenListFromFile)
        #self.menu.add_command(label = "Debug", command = self.debug)
        self.master.config(menu = self.menu)
 
        # self.B1 = Button(self.mainFrame, text = "Print", width = 8, command = self.display)
        # self.B1.pack(padx = 5, pady = 5, side = LEFT)
        # self.B2 = Button(self.mainFrame, text = "Clear", width = 8, command = self.clear)
        # self.B2.pack(padx = 5, pady = 5, side = LEFT)
        # self.B3 = Button(self.mainFrame, text = "Undo", width = 8, command = self.undo)
        # self.B3.pack(padx = 5, pady = 5, side = LEFT)
        # self.B4 = Button(self.mainFrame, text = "Redo", width = 8, command = self.redo)
        # self.B4.pack(padx = 5, pady = 5, side = LEFT)
        canvas.grid(row=0, column=0)

        # Making a Canvas
        canvas = Canvas(mainFrame, height=450, width=1000, bg="white")
        canvas.grid(row=0, column=0)
        canvas.place(relx=0.5, rely=0.5, anchor=CENTER)
        canvas.config(cursor="pencil")

        # Event Binding
        canvas.bind("<B1-Motion>", paint)
        canvas.bind("<ButtonRelease-1>", paint)
        canvas.bind("<Button-1>", paint)        
        self.mainFrame.pack(padx = 5, pady = 5, fill= BOTH)
 
    def display(self):
        print(self.sequenceTextBox.get("1.0", "end"))     

    def clear(self):
        self.sequenceTextBox.delete("1.0", "end")
 
    def stackify(self):
        self.stack.append(self.sequenceTextBox.get("1.0", "end - 1c"))
        if self.stackcursor < 9: self.stackcursor += 1
 
    def undo(self):
        if self.stackcursor != 0:
            self.clear()
            if self.stackcursor > 0: self.stackcursor -= 1
            self.sequenceTextBox.insert("0.0", self.stack[self.stackcursor])
 
    def redo(self):
        if len(self.stack) > self.stackcursor + 1:
            self.clear()
            if self.stackcursor < 9: self.stackcursor += 1
            self.sequenceTextBox.insert("0.0", self.stack[self.stackcursor])
 
    def printStack(self):
        i = 0
        for stack in self.stack:
            print(str(i) + " " + stack)
            i += 1
  

   
    # def showForbiddenListFromFile(self):
    #     listString=""
    #     for line in Controller.model.forbiddenList:
    #         listString+=line
    #     messagebox.showinfo("Forbidden list", listString+"                    ")

    # def debug(self):
    #     print("Model")
    #     print(Controller.model.dump())
    #     messagebox.showinfo("Model", Controller.model.dump())
        
    # end class    

def mainFrameUI(text:str):
    rootWindow = Tk()
    rootWindow.title('Robot Deck Simulation')
    rootWindow.geometry(str(rootWindow.winfo_screenwidth())+"x"+str( int(rootWindow.winfo_screenheight()*.7)))
    #rootWindow.state('zoomed')
    window = Window(rootWindow)
    #rootWindow.attributes('-fullscreen', True)
    #screen_width = win.winfo_screenwidth()
    rootWindow.bind("<Key>", lambda event: window.stackify())
    rootWindow.protocol( "WM_DELETE_WINDOW", onExit )
    rootWindow.mainFrameloop()


def onExit():
     #messagebox.showinfo("bye", "bye")
    #  UtilFileIO.saveModelToFile()
     #os.path.dirname(os.path.abspath(__file__))+"\\..\\default.fa"
     quit()
	
   
mainFrameUI("RobotDeck")


# from tkinter import * 
# from tkinter.ttk import *
 
# # creating tkinter window
# root = Tk()
# # getting screen's height in pixels
# height = root.winfo_screenheight()
# width = root.winfo_screenwidth()

# my_var = StringVar()
 
# # defining the callback function (observer)
# def my_callback(var, index, mode):
#     print (("Traced variable ".format(my_var.get())))
 
# # registering the observer
# my_var.trace_add('write', my_callback)
 
# Label(root, textvariable = my_var).pack(padx = 5, pady = 5)
 
# Entry(root, textvariable = my_var).pack(padx = 5, pady = 5)

# print("\n width x height = %d x %d (in pixels)\n" %(width, height))
# # infinite loop
# mainFrameloop()