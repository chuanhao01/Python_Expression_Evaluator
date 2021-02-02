
from ...nodes import *

class InOrder:
    @staticmethod
    def print_output(node):
        if node:
            InOrder.print_output(node.left_term)
            InOrder.print_output(node.token_value)
            InOrder.print_output(node.right_term)