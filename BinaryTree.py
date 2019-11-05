
import math


class TreeNode:

    def __init__(self, key, parent=None, left=None, right=None):
        self.key = key
        self.left = left
        self.right = right
        self.parent = parent

    def set_key(self, key):
        self.key = key

    def get_key(self):
        return self.key

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

    def get_tree_height(self):
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
        if parent.get_key() == node.key:
            raise ValueError
        elif parent.get_key() > node.key:
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

    def search(self, key, node):
        if node is None:
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

    def check_tree_balance(self, node):
        if node is None:
            return None, 0
        balance_factor = self.get_balance_factor(node)
        if (balance_factor < -1) or (balance_factor > 1):
            return node, balance_factor
        return self.check_tree_balance(node.get_left())
        return self.check_tree_balance(node.get_right())





















