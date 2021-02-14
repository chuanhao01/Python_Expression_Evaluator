'''
    This Python File deals with printing the expression in InOrder

    InOrder:
        left - root - right
'''

from ...nodes import NodeVisitor

class InOrder(NodeVisitor):
    def __init__(self, level = 0):
        self.__level = level

    #* Getter and Setter
    def get_level(self):
        return self.__level

    def set_level(self, level):
        self.__level = level


    def traverse(self, node):
        if type(node).__name__ == "BinaryOp_Node":
            # Left
            self.__level += 1
            self.traverse(node.left_term)

            # Root
            self.__level -= 1
            print(str("~" * self.__level) + " " + node.operator.token_value)
            
            # Right
            self.__level += 1
            self.traverse(node.right_term)

        elif type(node).__name__ == "Number_Node":
            print(str("~" * self.__level) + " " + str(node.token_value))
            return

        else:
            self.visit_error(node)