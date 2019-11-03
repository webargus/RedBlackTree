
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
        wrap.grid_rowconfigure(3, weight=5)
        wrap.grid_columnconfigure(0, weight=1)

        header = Frame(wrap)
        header.grid({"row": 0, "column": 0, "sticky": EW})
        l1 = Label(header, {"text": "Binary tree implementation",
                            "font": ("Arial", 12),
                            "pady": 4,
                            "padx": 4})
        l1.grid({"row": 0, "column": 0})

        frame_adding = LabelFrame(wrap, text=" Edit ", height=80)
        frame_adding.grid({"row": 1, "column": 0, "sticky": EW, "pady": 8, "padx":8})
        form = Frame(frame_adding, {"pady": 4, "padx": 8})
        form.grid({"row": 0, "column": 0, "sticky": NSEW, "pady": 8, "padx": 8})

        Label(form, text="Value:", font=("Arial", 10)).grid(row=0, column=0, sticky=W)
        self.node_value = StringVar()
        self.node_value_entry = Entry(form, font=("Arial", 10), width=5, textvar=self.node_value)
        self.node_value_entry.grid(row=0, column=1, sticky=W)
        self.node_add_btn = Button(form, text="Insert", font=("Arial", 10), width=5, command=self._add_node)
        self.node_add_btn.grid(row=0, column=2, sticky=W)

        self.max_button = Button(form,
                                   text="Maximum",
                                   font=("Arial", 10),
                                   width=8,
                                   command=self._maximum)
        self.max_button.grid(row=0, column=3, sticky=E)

        self.minimum_btn = Button(form,
                                   text="Minimum",
                                   font=("Arial", 10),
                                   width=8,
                                   command=self._minimum)
        self.minimum_btn.grid(row=0, column=4, sticky=E)

        self.successor_btn = Button(form,
                                   text="Successor",
                                   font=("Arial", 10),
                                   width=8,
                                   command=self._successor)
        self.successor_btn.grid(row=0, column=5, sticky=E)

        self.predecessor_btn = Button(form,
                                   text="Predecessor",
                                   font=("Arial", 10),
                                   width=8,
                                   command=self._predecessor)
        self.predecessor_btn.grid(row=0, column=6, sticky=E)

        # add frame and blank label just to create left margin before delete and clear btns
        spacer = Frame(form)
        spacer.grid(row=0, column=7, sticky=W)
        Label(spacer, text=" "*20).grid(row=0, column=0)

        self.del_node_btn = Button(form,
                                   text="Delete",
                                   font=("Arial", 10),
                                   width=8,
                                   state="disabled",
                                   command=self._delete)
        self.del_node_btn.grid(row=0, column=8, sticky=E)

        self.clear_tree_btn = Button(form,
                                     text="Clear",
                                     font=("Arial", 10),
                                     width=8,
                                     command=self._clear_tree)
        self.clear_tree_btn.grid(row=0, column=9, sticky=E)

        fb_frame = Frame(wrap, height=50)
        fb_frame.grid(row=2, column=0, sticky=EW, pady=4)
        # Feedback label
        self.feedback = StringVar()
        self.fb_label = Label(fb_frame, font=("Arial", 10), textvar=self.feedback)
        self.fb_label.grid(row=1, column=0, sticky=EW, padx=8)

        canvasF = Frame(wrap, {"relief": SUNKEN, "border": 1, "height": 500})
        canvasF.grid({"pady": 8, "padx": 8, "row": 3, "column": 0, "sticky": NSEW})
        canvasF.grid_columnconfigure(0, weight=1)
        canvasF.grid_rowconfigure(0, weight=1)
        # create BT canvas
        self.canvas = BinaryTreeCanvas.BinaryTreeCanvas(canvasF, self._feedback)
        self._clear_tree()

    def _add_node(self):
        try:
            value = int(self.node_value.get())
        except ValueError:
            messagebox.showerror("Invalid input", "Please, enter integers only")
            return
        self.canvas.add_node(value)
        self._feedback("Click on node to call BST search for node key")
        self._enable_btn(self.max_button)
        self._enable_btn(self.minimum_btn)
        self._enable_btn(self.clear_tree_btn)
        self._enable_btn(self.predecessor_btn, False)
        self._enable_btn(self.successor_btn, False)
        self._enable_btn(self.del_node_btn, False)

    def _clear_tree(self):
        self.canvas.clear_tree()
        self._feedback("Insert a node into BST")
        self._enable_btn(self.minimum_btn, False)
        self._enable_btn(self.max_button, False)
        self._enable_btn(self.predecessor_btn, False)
        self._enable_btn(self.successor_btn, False)
        self._enable_btn(self.del_node_btn, False)
        self._enable_btn(self.clear_tree_btn, False)

    def _maximum(self):
        self.canvas.maximum()

    def _minimum(self):
        self.canvas.minimum()

    def _successor(self):
        self.canvas.successor()

    def _predecessor(self):
        self.canvas.predecessor()

    def _delete(self):
        self.del_node_btn.configure(state="disabled")
        pass

    def _feedback(self, msg, sel=False):
        self.feedback.set(msg)
        if sel:                                 # user selected some node in GUI
            self._enable_btn(self.del_node_btn)
            self._enable_btn(self.successor_btn)
            self._enable_btn(self.predecessor_btn)

    def _enable_btn(self, btn, en=True):
        if en:
            btn.configure(state="normal")
        else:
            btn.configure(state="disabled")








