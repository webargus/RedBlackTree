
"""
    UFRPE - BSI2019.2 - Algorithms and Data Structures
    Author: Edson Kropniczki

"""

from tkinter import *
from tkinter.ttk import *
import BinaryTreePanel
import ScrollableText


class Gui(Frame):

    def __init__(self):
        Frame.__init__(self)
        self.imgicon = PhotoImage(file='icon32.png')
        self.master.tk.call('wm', 'iconphoto', self.master._w, self.imgicon)

        self.master.resizable(False, False)
        self.master.attributes("-zoomed", True)
        self.master.title("Algorithms and Data Structures' - SI2019.2")
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.grid({"row": 0, "column": 0, "sticky": NSEW})
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.nb = Notebook(self)
        #   add tabs
        self.nb_files = [("Binary Tree", Frame(self.nb), "BinaryTree")]
        for i in self.nb_files:
            self.nb.add(i[1], text="    " + i[0] + "    ")
        self.nb.grid({"row": 0, "column": 0, "sticky": NSEW})
        self.nb.bind("<<NotebookTabChanged>>", self._tab_switch)

        BinaryTreePanel.BinaryTreePanel(self.nb_files[0][1])

        frame = Frame(self)
        frame.grid({"row": 0, "column": 1, "sticky": NSEW, "pady": 4, "padx": 4})
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        ftop = Frame(frame)
        ftop.grid({"row": 0, "column": 0})
        text = "NOTICE: This is a rather simple, reusable hack of a standard tkinter Graphical User Interface template,"
        text += " geared towards facilitating user input in a graphical manner, when testing exercise assignments "
        text += "from the UFRPE Programming Lab subject program, as opposed to the otherwise cumbersome and "
        text += "far less efficient console-based input methods. All exercise source codes come in separated "
        text += "*.py package files which then again come listed in the "
        text += "text area section below just for the sake of easy reading and verification purposes.\n"
        text += "Therefore, having said that, please bear in mind that only source codes exclusively listed in "
        text += "the text area below "
        text += "should matter when analysing the solutions herein proposed for the exercise assignments, "
        text += "since the GUI code and the tkinter native code do not interfere in any ways or manners whatsoever "
        text += "neither with the solution proposed, its complexity level, nor with the code structure of the exercise."
        Label(ftop,
              text=text,
              wraplength=500,
              font=("Arial", 8),
              relief=RIDGE,
              padding=4).grid({"row": 0, "column": 0})
        fbottom = Frame(frame)
        fbottom.grid({"row": 1, "column": 0, "sticky": NSEW})
        self.text_widget = ScrollableText.ScrollableText(fbottom)

        self.mainloop()

    def _tab_switch(self, event):
        file = self.nb_files[self.nb.index(self.nb.select())][2] + ".py"
        try:
            handle = open(file, "r", encoding="utf-8")
        except OSError:
            print(OSError.args)
        self.text_widget.clear()
        self.text_widget.append_text("# Source file: %s\n" % file)
        for line in handle.readlines():
            self.text_widget.append_text(line)
        handle.close()


if __name__ == '__main__':
    gui = Gui()






