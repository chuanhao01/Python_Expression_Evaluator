'''
    This Python File deals with printing the expression in InOrder

    PreOrder:
        left - right - root
'''

from ...nodes import NodeVisitor

class PostOrder(NodeVisitor):
    @staticmethod
    def print_output(self, node, level = 0):
        level += 1

        # Left sub-tree
        if node.left_term != None:
            #PreOrder.print_output(node.left_term, level)
            self.visit(node.left_term)

        # Right sub-tree
        if node.right_term != None:
            #PreOrder.print_output(node.right_term, level)
            self.visit(node.right_term)

        # Root
        print(str(level * '~') +  str(node.token_value))
    

    # Overriding the original visit() method in NodeVisitor
    def visit(self, node, level):
        node_name = type(node).__name__
        method_name = f"visit_{node_name}"

        visit_method = getattr(self, method_name, self.visit_error)
        return visit_method(node, level)

    def visit_Number_Node(self, node, level):
        return node.token_value

    def visit_BinaryOp_Node(self, node, level):
        return PostOrder.print_output(node, level)