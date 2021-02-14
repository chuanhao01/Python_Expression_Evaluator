'''
    This Python File deals with printing the expression in PreOrder

    PreOrder:
        root - left - right
'''

from ...nodes import NodeVisitor

class PreOrder(NodeVisitor):
    def __init__(self, level = 0):
        self.__level = level

    #* Getter and Setter
    def get_level(self):
        return self.__level

    def set_level(self, level):
        self.__level = level


    def traverse(self, node):
        if type(node).__name__ == "BinaryOp_Node":
            # Root
            print(str("~" * self.__level) + " " + node.operator.token_value)
            self.__level += 1

            # Left
            self.traverse(node.left_term)
            
            # Right
            self.traverse(node.right_term)
            self.__level -= 1

        elif type(node).__name__ == "Number_Node":
            print(str("~" * self.__level) + " " + str(node.token_value))
            return

        else:
            self.visit_error(node)