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

        self.selected = self.sel_rect = self.tree = None

    def _handle_click(self, event):
        item = self.canvas.find_withtag("current")
        tags = self.canvas.gettags(item)
        if (len(tags) > 1) and (tags[0] == "node"):
            node = self.tree.search(int(tags[1]), self.tree.root)
            self._select_node(node)
            txt = "Search for key %s returned node [%s]" % (tags[1], str(node))
            self.callback(txt, True)

    def maximum(self):
        max_node = self.tree.maximum(self.tree.root)
        if max_node is None:
            self.callback("There is no maximum BST key")
        else:
            self._select_node(max_node)
            self.callback("Maximum BST key: %d" % max_node.get_key(), True)

    def minimum(self):
        min_node = self.tree.minimum(self.tree.root)
        if min_node is None:
            self.callback("There is no minimum BST key")
        else:
            self._select_node(min_node)
            self.callback("Minimum BST key: %d" % min_node.get_key(), True)

    def successor(self):
        node = self.selected
        if node is None:
            return
        successor = self.tree.successor(node)
        k = node.get_key()
        if successor is None:
            self.callback("There is no successor for %d, i.e., %d is the BST maximum" % (k, k))
        else:
            self.callback("The successor of %d is %d" % (k, successor.get_key()))

    def predecessor(self):
        node = self.selected
        if node is None:
            return
        predecessor = self.tree.predecessor(node)
        k = node.get_key()
        if predecessor is None:
            self.callback("There is no predecessor for %d, i.e., %d is the BST minimum" % (k, k))
        else:
            self.callback("The predecessor of %d is %d" % (k, predecessor.get_key()))

    def delete(self):
        node = self.selected
        if node is None:
            return
        self.callback("Deleting node %s..." % str(node))
        y = self.tree.delete(node)
        self._redraw_tree()
        self.balance_tree()

    def _select_node(self, node):
        self.canvas.coords(self.sel_rect,
                           (node.x - 1.5 * CanvasTreeNode.NODE_RADIUS,
                            node.y - 1.5 * CanvasTreeNode.NODE_RADIUS,
                            node.x + 1.5 * CanvasTreeNode.NODE_RADIUS,
                            node.y + 1.5 * CanvasTreeNode.NODE_RADIUS))

        self.canvas.itemconfigure(self.sel_rect, state="normal")
        self.selected = node

    def add_node(self, key):
        try:
            self.tree.add(CanvasTreeNode(key))
        except ValueError:
            self.callback("Insertion failed: key %d already exists" % key)
            return
        self._redraw_tree()
        self.callback("Click on a node to call BST search for node key")
        self.balance_tree()

    def balance_tree(self):
        unbalanced, factor = self.tree.check_tree_balance(self.tree.root)
        if unbalanced is None:
            print("tree balanced")
            return
        else:
            print("tree unbalanced at node %s, balance factor: %d" % (str(unbalanced), factor))
        if factor < 0:
            self.rotate_right(unbalanced)
        else:
            self.rotate_left(unbalanced)
        self._redraw_tree()

    def rotate_left(self, node):
        y = node.get_right()
        node.set_right(y.get_left())
        if y.get_left() is not None:
            y.get_left().set_parent(node)
        y.set_parent(node.get_parent())
        if node.get_parent() is None:
            self.tree.root = y
        elif node == node.get_parent().get_left():
            node.get_parent().set_left(y)
        else:
            node.get_parent().set_right(y)
        y.set_left(node)
        node.set_parent(y)


    def rotate_right(self, node):
        pass

    def _redraw_tree(self):
        self.clear()
        self.tree.pre_order_tree_walk(self.tree.root, self.draw_tree)

    def draw_tree(self, node):
        # print(node)             # debug
        width = self.canvas.winfo_width() - 2*CanvasTreeNode.NODE_RADIUS
        dx = 2*CanvasTreeNode.NODE_RADIUS
        parent = node.get_parent()
        if parent is None:                  # that's the root node
            node.x = width//2
            node.y = 2*dx
        else:
            const = dx*2**(self.tree.get_node_height(parent) - 1)
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

        self.canvas.create_oval(x - CanvasTreeNode.NODE_RADIUS,
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
        # draw balance factor
        parent = node.get_parent()
        sign = 1
        if parent is not None:
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
        self.tree = BinaryTree.BinaryTree()
        self.clear()

    def is_empty(self):
        return (self.tree is None) or (self.tree.n == 0)


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










