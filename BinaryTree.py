

class RBTreeNode:

    RED = "red"
    BLACK = "black"

    def __init__(self, key):
        self.key = key
        self.parent = self.left = self.right = None
        self.color = RBTreeNode.RED

    def get_uncle(self):
        if (self.parent is None) or (self.parent.parent is None):
            return None
        if self.parent.is_left():
            return self.parent.parent.right
        else:
            return self.parent.parent.left

    def is_left(self):
        return self == parent.left

    def sibling(self):
        if self.parent is None:
            return None
        if self.is_left():
            return self.parent.right
        return self.parent.left

    def put_down(self, parent):
        if parent is not None:
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
            if (u is not None) and (u.color == RBTreeNode.BLACK):
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

    def get_delete_rep(self, x):
        if (x.left is not None) and (x.right is not None):
            return self.successor(x.right)
        if (x.left is None) and (x.right is None):
            return None
        if x.left is None:
            return x.right
        else:
            return x.left

    def rb_delete(self, z):
        x = self.get_delete_rep(z)

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


