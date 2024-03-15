from tkinter import *
from tkinter import filedialog
from collections import deque
from tkinter import messagebox
 

class Window:
    def __init__(self, master):
        self.master = master
        self.Main = Frame(self.master)
        self.stack = deque(maxlen = 10)
        self.stackcursor = 0

        self.sequenceLabel = Label(self.Main, text = "Please load a Fasta File")
        self.sequenceLabel.pack(padx = 5, pady = 5)

        textScrollbar=Scrollbar(self.Main, orient='horizontal')
        textScrollbar.pack(side=BOTTOM, fill='x')  
        self.sequenceTextBox:Text = Text(self.Main, xscrollcommand=textScrollbar.set,wrap="none" )
        self.sequenceTextBox.edit
        #self.forbiddenList.pack(side= RIGHT, fill= BOTH)     
        self.sequenceTextBox.pack(padx = 5, pady = 5,fill= BOTH)
        textScrollbar.config(command=self.sequenceTextBox.xview)
        #text.pack()
        self.menu = Menu(self.Main)
        # self.menu.add_command(label = "Print", command = self.printStack)
        # self.menu.add_command(label = "Undo", command = self.undo)
        # self.menu.add_command(label = "Redo", command = self.redo)
        self.menu.add_command(label = "Domesticate", command = self.domesticate)
        #self.menu.add_command(label = "Show Forbidden", command = self.showForbiddenListFromFile)
        self.menu.add_command(label = "Debug", command = self.debug)
        self.master.config(menu = self.menu)
 
        # self.B1 = Button(self.Main, text = "Print", width = 8, command = self.display)
        # self.B1.pack(padx = 5, pady = 5, side = LEFT)
        # self.B2 = Button(self.Main, text = "Clear", width = 8, command = self.clear)
        # self.B2.pack(padx = 5, pady = 5, side = LEFT)
        # self.B3 = Button(self.Main, text = "Undo", width = 8, command = self.undo)
        # self.B3.pack(padx = 5, pady = 5, side = LEFT)
        # self.B4 = Button(self.Main, text = "Redo", width = 8, command = self.redo)
        # self.B4.pack(padx = 5, pady = 5, side = LEFT)
        self.Main.pack(padx = 5, pady = 5, fill= BOTH)
 
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
  
    def domesticate(self):
        rootWindow=self.master

   
    def showForbiddenListFromFile(self):
        listString=""
        for line in Controller.model.forbiddenList:
            listString+=line
        messagebox.showinfo("Forbidden list", listString+"                    ")

    def debug(self):
        print("Model")
        
    # end class    

def mainUI(text:str):
    rootWindow = Tk()
    rootWindow.title('Brick Designer')
    rootWindow.geometry(str(rootWindow.winfo_screenwidth())+"x"+str( int(rootWindow.winfo_screenheight()*.7)))
    #rootWindow.state('zoomed')
    window = Window(rootWindow)
    #rootWindow.attributes('-fullscreen', True)
    #screen_width = win.winfo_screenwidth()
    rootWindow.bind("<Key>", lambda event: window.stackify())
    rootWindow.protocol( "WM_DELETE_WINDOW", onExit )
    rootWindow.mainloop()


def onExit():
     #messagebox.showinfo("bye", "bye")
     #os.path.dirname(os.path.abspath(__file__))+"\\..\\default.fa"
     quit()
	
   

mainUI("dfdfgd")