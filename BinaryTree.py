
from collections import deque
import math


class TreeNode:

    def __init__(self, value, parent=None, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right
        self.parent = parent

    def get_value(self):
        return self.value

    def get_left(self):
        return self.left

    def get_right(self):
        return self.right

    def get_parent(self):
        return self.parent

    def set_left(self, left):
        self.left = left

    def set_right(self, right):
        self.right = right

    def set_parent(self, parent):
        self.parent = parent


class BinaryTree:

    def __init__(self):
        self.root = None
        self.n = 0

    def get_depth(self):
        if self.n == 0:
            return 0
        return math.ceil(math.log2(self.n))

    def add(self, node):
        self.n += 1
        if self.root is None:
            self.root = node
            return
        self._add(self.root, node)

    # @parent = node where we want to insert @node
    def _add(self, parent, node):
        if parent.get_value() > node.value:
            n = parent.get_left()
            if n is None:
                parent.set_left(node)
                node.set_parent(parent)
            else:
                self._add(n, node)
        else:
            n = parent.get_right()
            if n is None:
                parent.set_right(node)
                node.set_parent(parent)
            else:
                self._add(n, node)

    def in_order_tree_walk(self, node, callback):
        if node is None:
            return
        self.in_order_tree_walk(node.get_left(), callback)
        callback(node)              # do something with node
        self.in_order_tree_walk(node.get_right(), callback)

    def pre_order_tree_walk(self, node, callback):
        if node is None:
            return
        callback(node)
        self.pre_order_tree_walk(node.get_left(), callback)
        self.pre_order_tree_walk(node.get_right(), callback)

    def get_node_height(self, node):
        if node is None:
            return 0
        else:
            return max(self.get_node_height(node.get_left()), self.get_node_height(node.get_right())) + 1
































