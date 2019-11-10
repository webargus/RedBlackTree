

class RBTreeNode:
    
    RED = "red"
    BLACK = "black"

    def __init__(self, key):
        self.key = key
        self.left = self.right = self.parent = None
        self.color = RBTreeNode.RED


class BinaryTree:

    def __init__(self):
        self.root = None

    def get_root(self):
        return self.root

    def insert(self, node):
        y = None
        x = self.root
        while x is not None:
            y = x
            if node.key == x.key:
                raise ValueError
            elif node.key < x.key:
                x = x.left
            else:
                x = x.right
        node.parent = y
        if y is None:
            self.root = node
        elif node.key < y.key:
            y.left = node
        else:
            y.right = node
        self._rb_insert_fixup(node)

    def _rb_insert_fixup(self, node):
        if (node is not None) and (node.parent is not None):
            while node.parent.color == RBTreeNode.RED:
                if node.parent == node.parent.parent.left:
                    y = node.parent.parent.right
                    if y.color == RBTreeNode.RED:
                        node.parent.color = RBTreeNode.BLACK
                        y.color = RBTreeNode.BLACK
                        node.parent.parent.color = RBTreeNode.RED
                        node = node.parent.parent
                    elif node == node.parent.right:
                        node = node.parent
                        self.rotate_left(node)
                    node.parent.color = RBTreeNode.BLACK
                    grandpa = node.parent.parent
                    if (grandpa is not None) and (grandpa is not None):
                        grandpa.color = RBTreeNode.RED
                        self.rotate_right(grandpa)
                else:
                    y = node.parent.parent.left
                    if y.color == RBTreeNode.RED:
                        node.parent.color = RBTreeNode.BLACK
                        y.color = RBTreeNode.BLACK
                        node.parent.parent.color = RBTreeNode.RED
                        node = node.parent.parent
                    elif node == node.parent.left:
                        node = node.parent
                        self.rotate_right(node)
                    node.parent.color = RBTreeNode.BLACK
                    grandpa = node.parent.parent
                    if (grandpa is not None) and (grandpa is not None):
                        grandpa.color = RBTreeNode.RED
                        self.rotate_left(grandpa)
        self.root.color = RBTreeNode.BLACK

    def delete(self, z):

        if (z.left is None) or (z.right is None):
            y = z
        else:
            y = self.successor(z)
        if y.left is not None:
            x = y.left
        else:
            x = y.right
        x.parent = y.parent
        if y.parent is None:
            self.root = x
        elif y == y.parent.left:
            y.parent.left = x
        else:
            y.parent.right = x
        if y != z:
            z.key = y.key
            print("y = [%s], z = [%s]" % (y, z))
        if y.color == "black":
            self.__rb_delete_fixup(x)

        return y

    def __rb_transplant(self, u, v):
        if u.parent is None:
            v.parent = None
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
            v.parent = u.parent

    def __rb_delete_fixup(self, x):
        while (x != self.root) and (x.color == RBTreeNode.BLACK):
            print("x=%s" % x)
            if x == x.parent.left:
                w = x.parent.right
                if w.color == RBTreeNode.RED:
                    w.color = RBTreeNode.BLACK
                    x.parent.color = RBTreeNode.RED
                    self.rotate_left(x.parent)
                    w = x.parent.right
                if (w.left.color == RBTreeNode.BLACK) and (w.right.color == RBTreeNode.BLACK):
                    w.color = RBTreeNode.RED
                    x = x.parent
                else:
                    if w.right.color == RBTreeNode.BLACK:
                        w.left.color = RBTreeNode.BLACK
                        w.color = RBTreeNode.RED
                        self.rotate_right(w)
                        w = x.parent.right
                    w.set_color(x.parent.color)
                    x.parent.color = RBTreeNode.BLACK
                    w.right.color = RBTreeNode.BLACK
                    self.rotate_left(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.color == RBTreeNode.RED:
                    w.color = RBTreeNode.BLACK
                    x.parent.color = RBTreeNode.RED
                    self.rotate_right(x.parent)
                    w = x.parent.left
                if (w.right.color == RBTreeNode.BLACK) and (w.left.color == RBTreeNode.BLACK):
                    w.color = RBTreeNode.RED
                    x = x.parent
                else:
                    if w.left.color == RBTreeNode.BLACK:
                        w.right.color = RBTreeNode.BLACK
                        w.color = RBTreeNode.RED
                        self.rotate_left(w)
                        w = x.parent.left
                    w.color = x.parent.color
                    x.parent.color = RBTreeNode.BLACK
                    w.left.color = RBTreeNode.BLACK
                    self.rotate_right(x.parent)
                    x = self.root
        x.color = RBTreeNode.BLACK

    # left rotate                                    y
    #       x                                       / \
    #      / \                                     /   \
    #     Sx  y                     =>            x     z
    #        / \                                 / \   / \
    #      Sy   z                              Sx  Sy Szl Szr
    #          / \
    #        Szl  Szr

    def rotate_left(self, x):
        y = x.right
        x.right = y.left
        if y.left is not None:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def rotate_right(self, x):
        y = x.left
        x.left = y.right
        if (y.right is not None) and (y.right is not None):
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def in_order_tree_walk(self, node, callback):
        if node is None:
            return
        self.in_order_tree_walk(node.left, callback)
        callback(node)              # do something with node, like drawing it in a tkinter canvas
        self.in_order_tree_walk(node.right, callback)

    def pre_order_tree_walk(self, node, callback):
        if node is None:
            return
        callback(node)
        self.pre_order_tree_walk(node.left, callback)
        self.pre_order_tree_walk(node.right, callback)

    def search(self, key, node):
        if node is None:
            return node
        if key == node.key:
            return node
        elif key < node.key:
            return self.search(key, node.left)
        else:
            return self.search(key, node.right)

    # return maximum of subtree starting at @node
    def maximum(self, node):
        while node is not None:
            ret = node
            node = node.right
        return ret

    # return minimum of subtree starting at @node
    def minimum(self, node):
        while node is not None:
            ret = node
            node = node.left
        return ret

    # return successor of @node
    def successor(self, node):
        # just get the minimum of right subtree of node, if there is a right subtree
        n = node.right
        if n is not None:
            return self.minimum(n)
        # go up towards root otherwise, until we find a parent node
        # having a different right branch from current node
        n = node.parent
        while (n is not None) and (n.right == node):
            node = n
            n = node.parent
        return n

    # return de predecessor of @node
    def predecessor(self, node):
        # just get the maximum of left subtree of node, if there is a left subtree
        n = node.left
        if n is not None:
            return self.maximum(n)
        # go up towards BST root otherwise, until we find a parent node
        # having a different left branch from current node
        n = node.parent
        while (n is not None) and (n.left == node):
            node = n
            n = node.parent
        return n

    def get_node_height(self, node):
        if node is None:
            return -1
        else:
            return max(self.get_node_height(node.left), self.get_node_height(node.right)) + 1

    def get_balance_factor(self, node):
        return self.get_node_height(node.right) - self.get_node_height(node.left)





















