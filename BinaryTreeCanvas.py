from tkinter import *
import BinaryTree


class BinaryTreeCanvas:

    def __init__(self, frame, callback):
        # callback to send msgs back to caller
        self.callback = callback

        self.canvas = Canvas(frame, background="white", cursor="hand1")
        self.canvas.grid(row=0, column=0, sticky=NSEW)
        # add horizontal scrollbar
        hscroll = Scrollbar(frame, orient=HORIZONTAL, command=self.canvas.xview)
        hscroll.grid(row=1, column=0, sticky=EW)
        self.canvas.configure(xscrollcommand=hscroll.set)

        self.sel_rect = self.tree = None

    def _handle_click(self, event):
        item = self.canvas.find_withtag("current")
        tags = self.canvas.gettags(item)
        if (len(tags) > 1) and (tags[0] == "node"):
            node = self.tree.search(int(tags[1]), self.tree.root)
            self.canvas.coords(self.sel_rect,
                               (node.x-1.5*CanvasTreeNode.NODE_RADIUS,
                                node.y-1.5*CanvasTreeNode.NODE_RADIUS,
                                node.x+1.5*CanvasTreeNode.NODE_RADIUS,
                                node.y+1.5*CanvasTreeNode.NODE_RADIUS))
            self.canvas.itemconfigure(self.sel_rect, state="normal")
            txt = "Search for key %s returned node [%s]" % (tags[1], str(node))
            self.callback(txt, True)

    def add_node(self, value):
        self.tree.add(CanvasTreeNode(value))
        self.clear()
        self.tree.pre_order_tree_walk(self.tree.root, self.draw_tree)

    def draw_tree(self, node):
        # print(node)             # debug
        width = self.canvas.winfo_width() - 2*CanvasTreeNode.NODE_RADIUS
        dx = 2*CanvasTreeNode.NODE_RADIUS
        parent = node.get_parent()
        if parent is None:
            node.x = width//2
            node.y = dx
        else:
            const = dx*2**(self.tree.get_node_height(parent) - 2)
            node.x = parent.x
            if parent.get_left() == node:       # node belongs to left sub-tree
                node.x -= const
            else:
                node.x += const

            node.y = parent.y + 4*CanvasTreeNode.NODE_RADIUS

        self._draw_node(node, node.x, node.y)
        if parent is not None:
            self._draw_edge(parent, node)

    def _draw_node(self, node, x, y):
        key = node.get_key()

        circle = self.canvas.create_oval(x - CanvasTreeNode.NODE_RADIUS,
                                y - CanvasTreeNode.NODE_RADIUS,
                                x + CanvasTreeNode.NODE_RADIUS,
                                y + CanvasTreeNode.NODE_RADIUS,
                                fill="yellow")
        text = self.canvas.create_text(x,
                                y,
                                text=key,
                                font=CanvasTreeNode.FONT,
                                fill="blue",
                                activefill="red",
                                tags=("node", key))
        self.canvas.tag_bind(text, '<Button-1>', self._handle_click)

    def _draw_edge(self, node1,  node2):
        self.canvas.create_line(self._node_edge(node1, node2), self._node_edge(node2, node1), width=1)

    def _node_edge(self, node1, node2):
        d = ((node1.x - node2.x)**2 + (node1.y - node2.y)**2)**.5
        # watch out! possible division by zero here!!
        xp = node1.x + CanvasTreeNode.NODE_RADIUS * abs(node2.x - node1.x) / d
        yp = node1.y + CanvasTreeNode.NODE_RADIUS * abs(node2.y - node1.y) / d
        if node2.x < node1.x:
            xp = node1.x - (xp - node1.x)
        if node2.y < node1.y:
            yp = node1.y - (yp - node1.y)
        return xp, yp

    def clear(self):
        # delete all canvas items
        self.canvas.delete("all")
        # create selection rect
        self.sel_rect = self.canvas.create_rectangle(0, 0, 0, 0, outline="blue", width=2)
        self.canvas.itemconfigure(self.sel_rect, state="hidden")

    def clear_tree(self):
        self.tree = BinaryTree.BinaryTree()
        self.clear()


class CanvasTreeNode(BinaryTree.TreeNode):

    NODE_RADIUS = 10
    FONT = ("Arial", 10)

    def __init__(self, key, parent=None, left=None, right=None):
        super(CanvasTreeNode, self).__init__(key, parent, left, right)
        self.x = self.y = 0

    def __str__(self):
        s = "key: %s, " % self.get_key()
        s += "parent: %s, " % self._to_string(self.get_parent())
        s += "left child: %s, " % self._to_string(self.get_left())
        s += "right child: %s" % self._to_string(self.get_right())
        return s

    def _to_string(self, node):
        if node is None:
            txt = "None"
        else:
            txt = node.get_key()
        return txt










