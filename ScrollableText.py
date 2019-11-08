"""
    Class ScrollableText
    Author: Edson Kropniczki - kropniczki@gmail.com - (c) Jun/2019
    Disclaimer: use it on your own risk!
    License: feel free to mess up with it at will, provided you display this header in your code!
    Purpose: a tkinter Text widget fitted with a scrollbar
"""

from tkinter import *
import tkinter.ttk as ttk


class ScrollableText(Text):

    def __init__(self, frame):

        super(ScrollableText, self).__init__(frame)

        #   position Text widget on the left side of frame
        self.grid({"row": 0, "column": 0, "sticky": NSEW})
        #   insert vertical scrollbar
        vscroll = ttk.Scrollbar(frame, orient=VERTICAL, command=self.yview)
        vscroll.grid({"row": 0, "column": 1, "sticky": NS})
        self.configure(yscrollcommand=vscroll.set)
        # insert horizontal scrollbar
        hscroll = ttk.Scrollbar(frame, orient=HORIZONTAL, command=self.xview)
        hscroll.grid(row=1, column=0, sticky=EW)
        self.configure(xscrollcommand=hscroll.set, wrap=NONE)
        #   configure font for text
        self.tag_configure("font", font=('Arial', 10))
        #   make widget non-editable without disabling it
        self.bind("<Key>", lambda e: "break")

    def append_text(self, text):
        self.insert(END, text, 'font')

    def clear(self):
        self.delete('1.0', END)

    def set_text(self, text):
        self.delete()
        self.append_text(text)





