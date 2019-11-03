
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
        if sys.platform == 'win32':
            self.master.state("zoomed")
        else:
            self.master.attributes("-zoomed", True)
        self.master.title("Algorithms and Data Structures' - SI2019.2")
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.grid({"row": 0, "column": 0, "sticky": NSEW})
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        frame = Frame(self)
        frame.grid({"row": 0, "column": 0, "sticky": NS, "pady": 4, "padx": 4})
        frame.grid_rowconfigure(1, weight=1)

        ftop = Frame(frame)
        ftop.grid({"row": 0, "column": 0})
        text = "Please, refer to code below for checking Python BST implementation"
        Label(ftop,
              border=1,
              relief=SUNKEN,
              text=text,
              font=("Arial", 12),
              padding=4).grid({"row": 0, "column": 0, "pady": 4, "ipady": 4})
        fbottom = Frame(frame)
        fbottom.grid({"row": 1, "column": 0, "sticky": NSEW})
        fbottom.grid_rowconfigure(0, weight=1)
        self.text_widget = ScrollableText.ScrollableText(fbottom)
        # this is key to set width of entire left pane!
        self.text_widget.configure(width=60)

        self.nb = Notebook(self)
        #   add tabs
        self.nb_files = [("Binary Tree", Frame(self.nb), "BinaryTree")]
        for i in self.nb_files:
            self.nb.add(i[1], text="    " + i[0] + "    ")
        self.nb.grid({"row": 0, "column": 1, "sticky": NSEW})
        self.nb.bind("<<NotebookTabChanged>>", self._tab_switch)

        BinaryTreePanel.BinaryTreePanel(self.nb_files[0][1])


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






