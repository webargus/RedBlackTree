
import math


class TreeNode:

    def __init__(self, key, color="red", parent=None, left=None, right=None):
        self.__key = key
        self.__left = left
        self.__right = right
        self.__parent = parent
        self.__color = color

    def __str__(self):
        s = "key: %s, " % self._to_string(self.__key)
        s += "parent: %s, " % self._to_string(self.__parent)
        s += "left child: %s, " % self._to_string(self.__left)
        s += "right child: %s, " % self._to_string(self.__right)
        s += "color: %s" % self.__color
        return s

    def _to_string(self, x):
        if x is None:
            txt = "None"
        elif x == BinaryTree.NIL:
            txt = "T.nil"
        else:
            txt = x.get_key()
        return txt

    def __eq__(self, other):
        if other is None:
            return False

        if self.__key != other.get_key():
            return False

        # check right sub-tree
        if self.__right is None:
            if other.get_right() is not None:
                return False
        else:
            if other.get_right() is None:
                return False
            if self.__right.get_key() != other.get_right().get_key():
                return False

        # check left sub-tree
        if self.__left is None:
            if other.get_left() is not None:
                return False
        else:
            if other.get_left() is None:
                return False
            if self.__left.get_key() != other.get_left().get_key():
                return False

        # check parent sub-tree
        if self.__parent is None:
            if other.get_parent() is not None:
                return False
        else:
            if other.get_parent() is None:
                return False
            if self.__parent.get_key() != other.get_parent().get_key():
                return False

        return True

    def __ne__(self, other):
        return not self.__eq__(other)

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
        self.__root = BinaryTree.NIL
        self.n = 0

    def get_root(self):
        return self.__root

    def get_tree_height(self):
        if self.n == 0:
            return 0
        return math.ceil(math.log2(self.n))

    def insert(self, node):
        self.n += 1
        y = BinaryTree.NIL
        x = self.__root
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
            self.__root = node
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
        self.__root.set_color("black")

    def delete(self, z):
        """
        y = z
        y_original_color = y.get_color()
        if z.get_left() == BinaryTree.NIL:
            x = z.get_right()
            self.__rb_transplant(z, z.get_right())
        elif z.get_right() == BinaryTree.NIL:
            x = z.get_left()
            self.__rb_transplant(z, z.get_left())
        else:
            y = self.minimum(z.get_right())
            y_original_color = y.get_color()
            x = y.get_right()
            if y.get_parent() == z:
                x.set_parent(y)
            else:
                self.__rb_transplant(y, y.get_right())
                y.set_right(z.get_right())
                y.get_right().set_parent(y)
            self.__rb_transplant(z, y)
            y.set_left(z.get_left())
            y.get_left().set_parent(y)
            y.set_color(z.get_color())
        if y_original_color == "black":
            self.__rb_delete_fixup(x)

        """
        if (z.get_left() == BinaryTree.NIL) or (z.get_right() == BinaryTree.NIL):
            y = z
        else:
            y = self.successor(z)
        if y.get_left() != BinaryTree.NIL:
            x = y.get_left()
        else:
            x = y.get_right()
        x.set_parent(y.get_parent())
        if y.get_parent() == BinaryTree.NIL:
            self.__root = x
        elif y == y.get_parent().get_left():
            y.get_parent().set_left(x)
        else:
            y.get_parent().set_right(x)
        if y != z:
            z.set_key(y.get_key())
            print("y = [%s], z = [%s]" % (y, z))
            self.__rb_delete_fixup(z)
        if y.get_color() == "black":
            self.__rb_delete_fixup(x)
        return y

    def __rb_transplant(self, u, v):
        if u.get_parent() == BinaryTree.NIL:
            self.__root = v
        elif u == u.get_parent().get_left():
            u.get_parent().set_left(v)
        else:
            u.get_parent().set_right(v)
            v.set_parent(u.get_parent())

    def __rb_delete_fixup(self, x):
        while (x != self.__root) and (x.get_color() == "black"):
            print("x=%s" % x)
            if x == x.get_parent().get_left():
                w = x.get_parent().get_right()
                if w.get_color() == "red":
                    w.set_color("black")
                    x.get_parent().set_color("red")
                    self.rotate_left(x.get_parent())
                    w = x.get_parent().get_right()
                if (w.get_left().get_color() == "black") and (w.get_right().get_color() == "black"):
                    w.set_color("red")
                    x = x.get_parent()
                elif w.get_right().get_color() == "black":
                    w.get_left().set_color("black")
                    w.set_color("red")
                    self.rotate_right(w)
                    w = x.get_parent().get_right()
                    w.set_color(x.get_parent().get_color())
                    x.get_parent().set_color("black")
                    w.get_right().set_color("black")
                    self.rotate_left(x.get_parent())
                    x = self.__root
            else:
                w = x.get_parent().get_left()
                if w.get_color() == "red":
                    w.set_color("black")
                    x.get_parent().set_color("red")
                    self.rotate_right(x.get_parent())
                    w = x.get_parent().get_left()
                if (w.get_right().get_color() == "black") and (w.get_left().get_color() == "black"):
                    w.set_color("red")
                    x = x.get_parent()
                elif w.get_left().get_color() == "black":
                    w.get_right().set_color("black")
                    w.set_color("red")
                    self.rotate_left(w)
                    w = x.get_parent().get_left()
                    w.set_color(x.get_parent().get_color())
                    x.get_parent().set_color("black")
                    w.get_left().set_color("black")
                    self.rotate_right(x.get_parent())
                    x = self.__root
        x.set_color("black")

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
            self.__root = y
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
            self.__root = y
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
        while node != BinaryTree.NIL:
            ret = node
            node = node.get_right()
        return ret

    # return minimum of subtree starting at @node
    def minimum(self, node):
        while node != BinaryTree.NIL:
            ret = node
            node = node.get_left()
        return ret

    # return successor of @node
    def successor(self, node):
        # just get the minimum of right subtree of node, if there is a right subtree
        n = node.get_right()
        if n != BinaryTree.NIL:
            return self.minimum(n)
        # go up towards root otherwise, until we find a parent node
        # having a different right branch from current node
        n = node.get_parent()
        while (n != BinaryTree.NIL) and (n.get_right() == node):
            node = n
            n = node.get_parent()
        return n

    # return de predecessor of @node
    def predecessor(self, node):
        # just get the maximum of left subtree of node, if there is a left subtree
        n = node.get_left()
        if n != BinaryTree.NIL:
            return self.maximum(n)
        # go up towards BST root otherwise, until we find a parent node
        # having a different left branch from current node
        n = node.get_parent()
        while (n != BinaryTree.NIL) and (n.get_left() == node):
            node = n
            n = node.get_parent()
        return n

    def get_node_height(self, node):
        if node is None:
            return -1
        else:
            return max(self.get_node_height(node.get_left()), self.get_node_height(node.get_right())) + 1

    def get_balance_factor(self, node):
        return self.get_node_height(node.get_right()) - self.get_node_height(node.get_left())





















