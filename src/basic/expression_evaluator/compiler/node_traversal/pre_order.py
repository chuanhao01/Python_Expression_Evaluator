'''
    This Python File deals with printing the expression in PreOrder

    PreOrder:
        root - left - right
'''

from ...nodes import NodeVisitor

class PreOrder(NodeVisitor):
    def __init__(self, level = 0):
        self.level = level

    def traverse(self, node):
        if type(node).__name__ == "BinaryOp_Node":
            # Root
            print(str("~" * self.level) + " " + node.operator.token_value)
            self.level += 1

            # Left
            self.traverse(node.left_term)
            
            # Right
            self.traverse(node.right_term)
            self.level -= 1

        elif type(node).__name__ == "Number_Node":
            print(str("~" * self.level) + " " + str(node.token_value))
            return

        else:
            self.visit_error(node)