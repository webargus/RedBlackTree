from tkinter import *
import BinaryTree
import math


class BinaryTreeCanvas:

    def __init__(self, frame):

        self.canvas = Canvas(frame, background="white", cursor="tcross")
        self.canvas.grid(row=0, column=0, sticky=NSEW)
        self.max_height = self.max_width = self.scale = 0

        self.tree = None
        self.clear()

    def add_node(self, value):
        self.tree.add(CanvasTreeNode(value))
        self.canvas.delete("all")
        self.tree.breadth_first_search(self.tree.root, self.draw_tree)

    def draw_tree(self, node):
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
        self.canvas.create_oval(x - CanvasTreeNode.NODE_RADIUS,
                                y - CanvasTreeNode.NODE_RADIUS,
                                x + CanvasTreeNode.NODE_RADIUS,
                                y + CanvasTreeNode.NODE_RADIUS,
                                fill="yellow")

        if node is None:
            text = "None"
        else:
            text = node.get_value()
        self.canvas.create_text(x, y, text=text, font=CanvasTreeNode.FONT, fill="blue")

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
        self.tree = BinaryTree.BinaryTree()
        self.canvas.delete("all")


class CanvasTreeNode(BinaryTree.TreeNode):

    NODE_RADIUS = 10
    FONT = ("Arial", 10)

    def __init__(self, value, parent=None, left=None, right=None):
        super(CanvasTreeNode, self).__init__(value, parent, left, right)
        self.x = self.y = 0













