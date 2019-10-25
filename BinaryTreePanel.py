
from tkinter import *
from tkinter import messagebox
import BinaryTreeCanvas


class BinaryTreePanel:

    def __init__(self, frame):

        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        wrap = Frame(frame)
        wrap.grid({"row": 0, "column": 0, "sticky": NSEW})
        wrap.grid_rowconfigure(2, weight=1)
        wrap.grid_columnconfigure(0, weight=1)

        header = Frame(wrap)
        header.grid({"row": 0, "column": 0, "sticky": NSEW})
        l1 = Label(header, {"text": "Binary tree implementation",
                            "font": ("Arial", 12),
                            "pady": 4,
                            "padx": 4})
        l1.grid({"row": 0, "column": 0})

        form = Frame(wrap, {"pady": 4, "padx": 8})
        form.grid({"row": 1, "column": 0, "sticky": NSEW, "pady": 8, "padx": 8})
        # form.grid_columnconfigure(0, weight=1)

        Label(form, text="Value:", font=("Arial", 10)).grid(row=0, column=0, sticky=W)
        self.node_value = StringVar()
        self.node_value_entry = Entry(form, font=("Arial", 10), width=5, textvar=self.node_value)
        self.node_value_entry.grid(row=0, column=1, sticky=W)
        self.node_add_btn = Button(form, text="Add", font=("Arial", 10), width=5, command=self._add_node)
        self.node_add_btn.grid(row=0, column=2, sticky=W)
        self.clear_tree_btn = Button(form, text="Clear", font=("Arial", 10), width=5, command=self._clear_tree)
        self.clear_tree_btn.grid(row=0, column=3, sticky=W)

        canvasF = Frame(wrap, {"relief": SUNKEN, "border": 1})
        canvasF.grid({"pady": 8, "padx": 8, "row": 2, "column": 0, "sticky": NSEW})
        canvasF.grid_columnconfigure(0, weight=1)
        canvasF.grid_rowconfigure(0, weight=1)
        # create map canvas
        self.canvas = BinaryTreeCanvas.BinaryTreeCanvas(canvasF)

    def _add_node(self):
        try:
            value = int(self.node_value.get())
        except ValueError:
            messagebox.showerror("Invalid input", "Please, enter integers only")
            return
        self.canvas.add_node(value)

    def _clear_tree(self):
        self.canvas.clear()




