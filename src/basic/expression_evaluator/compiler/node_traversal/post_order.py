
from ...nodes import *

class PostOrder:
    @staticmethod
    def print_output(node):
        if node:
            PostOrder.print_output(node.left_term)
            PostOrder.print_output(node.right_term)
            PostOrder.print_output(node.token_value)