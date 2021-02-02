
from ...nodes import *

class PreOrder:
    @staticmethod
    def print_output(node):
        if node:
            PreOrder.print_output(node.token_value)
            PreOrder.print_output(node.left_term)
            PreOrder.print_output(node.right_term)