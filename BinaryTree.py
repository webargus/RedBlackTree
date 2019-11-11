
"""
UFRPE - BSI 2019.2 - Algorithms & Data Structures - prof. Tiago Espíndola
Project Red-Black Binary Search Tree
Author: Edson Kropniczki    -   kropniczki@gmail.com
License: free
Disclaimer: use it at your own risk
References:
    https://www.cs.purdue.edu/homes/ayg/CS251/slides/chap13c.pdf
    Thomas Cormen & co-authors - Introduction to Algorithms - third edition
"""


class RBTreeNode:

    RED = "red"
    BLACK = "black"

    def __init__(self, key):
        self.key = key
        self.parent = self.left = self.right = None
        self.color = RBTreeNode.RED

    def delete(self):
        """if self.parent is not None:
            if self.is_left():
                self.parent.left = None
            else:
                self.parent.right = None
        if self.right is not None:
            self.right.parent = None
        if self.left is not None:
            self.left.parent = None"""
        self.key = self.parent = self.left = self.right = self.color = None

    def get_uncle(self):
        if (self.parent is None) or (self.parent.parent is None):
            return None
        if self.parent.is_left():
            return self.parent.parent.right
        else:
            return self.parent.parent.left

    def is_left(self):
        if self.parent is not None:
            return self == self.parent.left
        return None

    def get_sibling(self):
        if self.parent is None:
            return None
        if self.is_left():
            return self.parent.right
        return self.parent.left

    def put_down(self, parent):
        if self.parent is not None:
            if self.is_left():
                self.parent.left = parent
            else:
                self.parent.right = parent
        parent.parent = self.parent
        self.parent = parent

    def is_child_red(self):
        b1 = (self.left is not None) and (self.left.color == RBTreeNode.RED)
        b2 = (self.right is not None) and (self.right.color == RBTreeNode.RED)
        return b1 or b2


class BinaryTree:

    def __init__(self):
        self.root = None

    def get_root(self):
        return self.root

    def rb_left_rotate(self, x):
        # make parent right child of node
        p = x.right
        if x == self.root:
            self.root = p
        x.put_down(p)
        # make right node of x left node of parent
        x.right = p.left
        # make x parent of left child (if parent had a left child)
        if p.left is not None:
            p.left.parent = x
        p.left = x

    def rb_right_rotate(self, x):
        p = x.left
        if x == self.root:
            self.root = p
        x.put_down(p)
        x.left = p.right
        if p.right is not None:
            p.right.parent = x
        p.right = x

    def rb_fix_up_red(self, x):
        # always set root color as black
        if x == self.root:
            x.color = RBTreeNode.BLACK
            return
        p = x.parent                    # p = parent of x
        gp = p.parent                   # gp = grand parent of x
        u = x.get_uncle()
        if p.color != RBTreeNode.BLACK:
            if (u is not None) and (u.color == RBTreeNode.RED):
                p.color = RBTreeNode.BLACK
                gp.color = RBTreeNode.RED
                u.color = RBTreeNode.BLACK
                self.rb_fix_up_red(gp)
            else:
                if p.is_left():
                    if x.is_left():
                        p.color, gp.color = (gp.color, p.color)
                    else:
                        self.rb_left_rotate(p)
                        x.color, gp.color = (gp.color, x.color)
                    self.rb_right_rotate(gp)
                else:
                    if x.is_left():
                        self.rb_right_rotate(p)
                        x.color, gp.color = (gp.color, x.color)
                    else:
                        p.color, gp.color = (gp.color, p.color)
                    self.rb_left_rotate(gp)

    def rb_fix_up_black(self, x):
        if x == self.root:
            return
        s = x.get_sibling()
        p = x.parent
        if s is None:
            self.rb_fix_up_black(p)
        else:
            if s.color == RBTreeNode.RED:
                p.color = RBTreeNode.RED
                s.color = RBTreeNode.BLACK
                if s.is_left():
                    self.rb_right_rotate(p)
                else:
                    self.rb_left_rotate(p)
                self.rb_fix_up_black(x)
            else:
                if s.is_child_red():
                    if (s.left is not None) and (s.left.color == RBTreeNode.RED):
                        if s.is_left():
                            s.left.color = s.color
                            s.color = p.color
                            self.rb_right_rotate(p)
                        else:
                            s.left.color = p.color
                            self.rb_right_rotate(s)
                            self.rb_left_rotate(p)
                    else:
                        if s.is_left():
                            s.right.color = p.color
                            self.rb_left_rotate(s)
                            self.rb_right_rotate(p)
                        else:
                            s.right.color = s.color
                            s.color = p.color
                            self.rb_left_rotate(p)
                    p.color = RBTreeNode.BLACK
                else:
                    s.color = RBTreeNode.RED
                    if p.color == RBTreeNode.BLACK:
                        self.rb_fix_up_black(p)
                    else:
                        p.color = RBTreeNode.BLACK

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
        self.rb_fix_up_red(node)

    def rb_delete(self, z):
        x = z.left
        if x is not None:
            x = self.maximum(x)
        if x is None:
            x = z.right
            if x is not None:
                x = self.minimum(x)
        both_black = ((x is None) or (x.color == RBTreeNode.BLACK)) and (z.color == RBTreeNode.BLACK)
        p = z.parent
        if x is None:
            if z == self.root:
                self.root.delete()
                self.root = None
            else:
                if both_black:
                    self.rb_fix_up_black(z)
                else:
                    if z.get_sibling() is not None:
                        z.get_sibling().color = RBTreeNode.RED
                if z.is_left():
                    p.left = None
                else:
                    p.right = None
            z.delete()
            return

        if (z.left is None) or (z.right is None):
            if z == self.root:
                z.key = x.key
                z.left = None
                z.right = None
                x.delete()
            else:
                if z.is_left():
                    p.left = x
                else:
                    p.right = x
                z.delete()
                x.parent = p
                if both_black:
                    self.rb_fix_up_black(x)
                else:
                    x.color = RBTreeNode.BLACK
            return
        x.key, z.key = (z.key, x.key)
        self.rb_delete(x)

    def pre_order_tree_walk(self, node, callback):
        if node is None:
            return
        callback(node)
        self.pre_order_tree_walk(node.left, callback)
        self.pre_order_tree_walk(node.right, callback)

    def search(self, key, node):
        if node is None:
            return node
        if int(key) == int(node.key):
            return node
        elif int(key) < int(node.key):
            return self.search(key, node.left)
        else:
            return self.search(key, node.right)

    # return maximum of subtree starting at @node
    def maximum(self, node):
        ret = None
        while node is not None:
            ret = node
            node = node.right
        return ret

    # return minimum of subtree starting at @node
    def minimum(self, node):
        ret = None
        while node is not None:
            ret = node
            node = node.left
        return ret

    # return successor of @node
    def successor(self, node):
        # just get the minimum of right subtree of node,
        # if there is a right subtree
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


