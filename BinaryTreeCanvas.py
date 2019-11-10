from tkinter import *
import RedBlackBinaryTree as rbt
import math


class BinaryTreeCanvas:

    def __init__(self, frame, callback):
        # callback to send msgs back to caller
        self.callback = callback

        self.canvas = Canvas(frame, background="white", cursor="hand1")
        self.canvas.grid(row=0, column=0, sticky=NSEW)
        # insert horizontal scrollbar
        hscroll = Scrollbar(frame, orient=HORIZONTAL, command=self.canvas.xview)
        hscroll.grid(row=1, column=0, sticky=EW)
        self.canvas.configure(xscrollcommand=hscroll.set)

        self.selected = self.sel_rect = None
        self.tree = rbt.BinaryTree()

    def _handle_click(self, event):
        item = self.canvas.find_withtag("current")
        tags = self.canvas.gettags(item)
        if (len(tags) > 1) and (tags[0] == "node"):
            node = self.tree.search(int(tags[1]), self.tree.get_root())
            self._select_node(node)
            txt = "Search for key %s returned node [%s]" % (tags[1], str(node))
            self.callback(txt)

    def maximum(self):
        root = self.tree.get_root()
        if root == rbt.BinaryTree.NIL:
            return
        max_node = self.tree.maximum(root)
        if max_node == rbt.BinaryTree.NIL:
            self.callback("There is no maximum BST key")
        else:
            self._select_node(max_node)
            self.callback("Maximum BST key: %d" % max_node.get_key())

    def minimum(self):
        root = self.tree.get_root()
        if root == rbt.BinaryTree.NIL:
            return
        min_node = self.tree.minimum(root)
        if min_node == rbt.BinaryTree.NIL:
            self.callback("There is no minimum BST key")
        else:
            self._select_node(min_node)
            self.callback("Minimum BST key: %d" % min_node.get_key())

    def successor(self):
        node = self.selected
        if node is None:
            return
        successor = self.tree.successor(node)
        k = node.get_key()
        if successor == rbt.BinaryTree.NIL:
            self.callback("There is no successor for %d, i.e., %d is the BST maximum" % (k, k))
        else:
            self.callback("The successor of %d is %d" % (k, successor.get_key()))

    def predecessor(self):
        node = self.selected
        if node is None:
            return
        predecessor = self.tree.predecessor(node)
        k = node.get_key()
        if predecessor == rbt.BinaryTree.NIL:
            self.callback("There is no predecessor for %d, i.e., %d is the BST minimum" % (k, k))
        else:
            self.callback("The predecessor of %d is %d" % (k, predecessor.get_key()))

    def delete(self):
        node = self.selected
        if node is None:
            return
        print("node to delete: [%s]" % node)
        self.tree.delete(node)
        if self.is_empty():
            self.clear_tree()
        else:
            self._redraw_tree()
        self.callback("Deleted node [%s]" % str(node))

    def _select_node(self, node):
        self.canvas.coords(self.sel_rect,
                           (node.x - 1.5 * CanvasTreeNode.NODE_RADIUS,
                            node.y - 1.5 * CanvasTreeNode.NODE_RADIUS,
                            node.x + 1.5 * CanvasTreeNode.NODE_RADIUS,
                            node.y + 1.5 * CanvasTreeNode.NODE_RADIUS))

        self.canvas.itemconfigure(self.sel_rect, state="normal")
        self.selected = node

    def insert_node(self, key):
        node = CanvasTreeNode(key)
        try:
            self.tree.insert(node)
        except ValueError:
            self.callback("Insertion failed: key %d already exists" % key)
            return True
        self._redraw_tree()
        self.callback("Click on a node to call BST search for node key and prompt it for operations")

    def _redraw_tree(self):
        self.clear()
        self.tree.pre_order_tree_walk(self.tree.get_root(), self.draw_tree)
        print("_"*30)

    def draw_tree(self, node):
        print(node)             # debug
        width = self.canvas.winfo_width() - 2*CanvasTreeNode.NODE_RADIUS
        dx = 2*CanvasTreeNode.NODE_RADIUS
        parent = node.get_parent()
        if parent == rbt.BinaryTree.NIL:                  # that's the root node
            node.x = width//2
            node.y = 2*dx
        else:
            h = self.tree.get_node_height(parent)
            const = dx*1.8**(h-h**.2)
            node.x = parent.x
            if parent.get_left() == node:       # node belongs to left sub-tree
                node.x -= const
            else:
                node.x += const

            node.y = parent.y + 4*CanvasTreeNode.NODE_RADIUS

        self._draw_node(node, node.x, node.y)
        if parent == rbt.BinaryTree.NIL:
            return
        self._draw_edge(parent, node)

    def _draw_node(self, node, x, y):
        key = node.get_key()

        self.canvas.create_oval(x - CanvasTreeNode.NODE_RADIUS,
                                y - CanvasTreeNode.NODE_RADIUS,
                                x + CanvasTreeNode.NODE_RADIUS,
                                y + CanvasTreeNode.NODE_RADIUS,
                                fill=node.get_color(),
                                outline="orange")
        text = self.canvas.create_text(x,
                                y,
                                text=key,
                                font=CanvasTreeNode.FONT,
                                fill="white",
                                activefill="yellow",
                                tags=("node", key))
        # draw balance factor
        parent = node.get_parent()
        sign = 1
        if parent != rbt.BinaryTree.NIL:
            sign = -1 + 2*(parent.get_right() == node)
        self.canvas.create_rectangle(x+.8*sign*CanvasTreeNode.NODE_RADIUS,
                                     y-2*CanvasTreeNode.NODE_RADIUS,
                                     x+2*sign*CanvasTreeNode.NODE_RADIUS,
                                     y-.8*CanvasTreeNode.NODE_RADIUS)
        self.canvas.create_text(x+1.4*sign*CanvasTreeNode.NODE_RADIUS,
                                y-1.4*CanvasTreeNode.NODE_RADIUS,
                                text=self.tree.get_balance_factor(node),
                                font=CanvasTreeNode.FONT)
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
        # reset node selection
        self.selected = None

    def clear_tree(self):
        self.tree = rbt.BinaryTree()
        self.clear()

    def is_empty(self):
        return self.tree.get_root() == rbt.BinaryTree.NIL


class CanvasTreeNode(rbt.TreeNode):

    NODE_RADIUS = 12
    FONT = ("Arial", 10)

    def __init__(self, key, color="red"):

        super(CanvasTreeNode, self).__init__(key, color, rbt.BinaryTree.NIL, rbt.BinaryTree.NIL, rbt.BinaryTree.NIL)
        self.x = self.y = 0

    def __str__(self):
        s = "key: %s, " % self.get_key()
        s += "parent: %s, " % self._to_string(self.get_parent())
        s += "left child: %s, " % self._to_string(self.get_left())
        s += "right child: %s," % self._to_string(self.get_right())
        s += "color: %s " % self.get_color()
        return s











