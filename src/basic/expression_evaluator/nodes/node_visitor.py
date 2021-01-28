
'''
This is the Python File containing the NodeVisitor class used for the Interpreter
'''

class NodeVisitor(object):
    def __init__(self, parser):
        self.parser = parser

    def visit_error(self, node):
        node_name = type(node).__name__
        raise NotImplementedError(f"visit_{node_name} has not been implemented yet!!")

    def visit(self, node):
        node_name = type(node).__name__
        method_name = f"visit_{node_name}"

        visit_method = getattr(self, method_name, self.visit_error)
        return visit_method(node)