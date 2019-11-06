
import BinaryTree


class RedBlackTreeNode(BinaryTree.TreeNode):

    def __init__(self, key, color, parent=None, left=None, right=None):
        super(RedBlackTreeNode, self).__init__(key, parent, left, right)
        self.color = color

    def get_color(self):
        return self.color


class RedBlackBinaryTree(BinaryTree.BinaryTree):

    def __init__(self):
        super(RedBlackBinaryTree, self).__init__()






