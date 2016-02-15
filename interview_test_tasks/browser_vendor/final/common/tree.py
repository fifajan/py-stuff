"""Module provides:

 - generic TreeNode;
 - string-valued TreeStringNode;
 - max-2-children BinaryTreeNode.
"""

class TreeNode(object):
    def __init__(self, value, *children): # *children here is like *args. 
        self.value = value
        self.children = [
            ch for ch in children if issubclass(ch.__class__, self.__class__)]
        if len(self.children) < len(children):
            print 'INFO: Auto-removed non TreeNode children.'

    def __str__(self):
        return repr(self)


class TreeStringNode(TreeNode):
    def __init__(self, value, *children):
        value = str(value)
        assert value != '\n'
        super(TreeStringNode, self).__init__(value, *children)


class BinaryTreeNode(TreeNode):
    def __init__(self, value, *children):
        if len(children) > 2:
            raise ValueError('More than 2 children in binary tree.')
        super(BinaryTreeNode, self).__init__(value, *children)
