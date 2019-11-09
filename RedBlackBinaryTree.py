
import math


class TreeNode:

    def __init__(self, key, color="red", parent=None, left=None, right=None):
        self.__key = key
        self.__left = left
        self.__right = right
        self.__parent = parent
        self.__color = color

    def set_key(self, key):
        self.__key = key

    def get_key(self):
        return self.__key

    def set_color(self, color):
        self.__color = color

    def get_color(self):
        return self.__color

    def get_left(self):
        return self.__left

    def get_right(self):
        return self.__right

    def get_parent(self):
        return self.__parent

    def set_left(self, left):
        self.__left = left

    def set_right(self, right):
        self.__right = right

    def set_parent(self, parent):
        self.__parent = parent


class BinaryTree:

    NIL = TreeNode(None, "black")

    def __init__(self):
        self.root = BinaryTree.NIL
        self.n = 0

    def get_tree_height(self):
        if self.n == 0:
            return 0
        return math.ceil(math.log2(self.n))

    def insert(self, node):
        self.n += 1
        y = BinaryTree.NIL
        x = self.root
        while x != BinaryTree.NIL:
            y = x
            if node.get_key() == x.get_key():
                raise ValueError
            elif node.get_key() < x.get_key():
                x = x.get_left()
            else:
                x = x.get_right()
        node.set_parent(y)
        if y == BinaryTree.NIL:
            self.root = node
        elif node.get_key() < y.get_key():
            y.set_left(node)
        else:
            y.set_right(node)
        node.set_left(BinaryTree.NIL)
        node.set_right(BinaryTree.NIL)
        self._rb_insert_fixup(node)

    def _rb_insert_fixup(self, node):
        while node.get_parent().get_color() == "red":
            if node.get_parent() == node.get_parent().get_parent().get_left():
                y = node.get_parent().get_parent().get_right()
                if y.get_color() == "red":
                    node.get_parent().set_color("black")
                    y.set_color("black")
                    node.get_parent().get_parent().set_color("red")
                    node = node.get_parent().get_parent()
                elif node == node.get_parent().get_right():
                    node = node.get_parent()
                    self.rotate_left(node)
                node.get_parent().set_color("black")
                grandpa = node.get_parent().get_parent()
                if (grandpa != BinaryTree.NIL) and (grandpa is not None):
                    grandpa.set_color("red")
                    self.rotate_right(grandpa)
            else:
                y = node.get_parent().get_parent().get_left()
                if y.get_color() == "red":
                    node.get_parent().set_color("black")
                    y.set_color("black")
                    node.get_parent().get_parent().set_color("red")
                    node = node.get_parent().get_parent()
                elif node == node.get_parent().get_left():
                    node = node.get_parent()
                    self.rotate_right(node)
                node.get_parent().set_color("black")
                grandpa = node.get_parent().get_parent()
                if (grandpa != BinaryTree.NIL) and (grandpa is not None):
                    grandpa.set_color("red")
                    self.rotate_left(grandpa)
        self.root.set_color("black")

    # left rotate                                    y
    #       x                                       / \
    #      / \                                     /   \
    #     Sx  y                     =>            x     z
    #        / \                                 / \   / \
    #      Sy   z                              Sx  Sy Szl Szr
    #          / \
    #        Szl  Szr

    def rotate_left(self, x):
        y = x.get_right()
        x.set_right(y.get_left())
        if y.get_left() != BinaryTree.NIL:
            y.get_left().set_parent(x)
        y.set_parent(x.get_parent())
        if x.get_parent() == BinaryTree.NIL:
            self.root = y
        elif x == x.get_parent().get_left():
            x.get_parent().set_left(y)
        else:
            x.get_parent().set_right(y)
        y.set_left(x)
        x.set_parent(y)

    def rotate_right(self, x):
        y = x.get_left()
        x.set_left(y.get_right())
        if y.get_right() != BinaryTree.NIL:
            y.get_right().set_parent(x)
        y.set_parent(x.get_parent())
        if x.get_parent() == BinaryTree.NIL:
            self.root = y
        elif x == x.get_parent().get_right():
            x.get_parent().set_right(y)
        else:
            x.get_parent().set_left(y)
        y.set_right(x)
        x.set_parent(y)

    def in_order_tree_walk(self, node, callback):
        if node == BinaryTree.NIL:
            return
        self.in_order_tree_walk(node.get_left(), callback)
        callback(node)              # do something with node, like drawing it in a tkinter canvas
        self.in_order_tree_walk(node.get_right(), callback)

    def pre_order_tree_walk(self, node, callback):
        if node == BinaryTree.NIL:
            return
        callback(node)
        self.pre_order_tree_walk(node.get_left(), callback)
        self.pre_order_tree_walk(node.get_right(), callback)

    def search(self, key, node):
        if node == BinaryTree.NIL:
            return node
        k = node.get_key()
        if key == k:
            return node
        elif key < k:
            return self.search(key, node.get_left())
        else:
            return self.search(key, node.get_right())

    # return maximum of subtree starting at @node
    def maximum(self, node):
        while node is not None:
            ret = node
            node = node.get_right()
        return ret

    # return minimum of subtree starting at @node
    def minimum(self, node):
        while node is not None:
            ret = node
            node = node.get_left()
        return ret

    # return successor of @node
    def successor(self, node):
        # just get the minimum of right subtree of node, if there is a right subtree
        n = node.get_right()
        if n is not None:
            return self.minimum(n)
        # go up towards root otherwise, until we find a parent node
        # having a different right branch from current node
        n = node.get_parent()
        while (n is not None) and (n.get_right() == node):
            node = n
            n = node.get_parent()
        return n

    # return de predecessor of @node
    def predecessor(self, node):
        # just get the maximum of left subtree of node, if there is a left subtree
        n = node.get_left()
        if n is not None:
            return self.maximum(n)
        # go up towards BST root otherwise, until we find a parent node
        # having a different left branch from current node
        n = node.get_parent()
        while (n is not None) and (n.get_left() == node):
            node = n
            n = node.get_parent()
        return n

    def delete(self, node):
        left = node.get_left()
        right = node.get_right()
        if (left is None) or (right is None):
            y = node
        else:
            y = self.successor(node)
        w = y.get_left()
        if w is not None:
            x = w
        else:
            x = y.get_right()
        w = y.get_parent()
        if x is not None:
            x.set_parent(w)
        if w is None:
            self.root = x
        elif y == w.get_left():
            w.set_left(x)
        else:
            w.set_right(x)
        if y != node:
            node.set_key(y.get_key())
        self.n -= 1
        return y

    def get_node_height(self, node):
        if node is None:
            return -1
        else:
            return max(self.get_node_height(node.get_left()), self.get_node_height(node.get_right())) + 1

    def get_balance_factor(self, node):
        return self.get_node_height(node.get_right()) - self.get_node_height(node.get_left())





















