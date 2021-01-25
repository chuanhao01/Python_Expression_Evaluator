
# * Basic Stack class implementation ( Stack == LIFO principle )
class Stack:
    def __init__(self):
        self.__list = []

    def isEmpty(self):
        return self.__list == []

    def size(self):
        return len(self.__list)

    def clear(self):
        self.__list.clear()

    def push(self, item):
        self.__list.append(item)

    def pop(self):
        if self.isEmpty():
            return None

        else:
            return self.__list.pop()

    def get(self):
        if self.isEmpty():
            return None

        else:
            return self.__list[-1]



# * Binary Tree Class
class BinaryTree:
    def __init__(self, key, leftTree=None, rightTree=None):
        self.key = key
        self.leftTree = leftTree
        self.rightTree = rightTree

    def setKey(self, key):
        self.key = key

    def getKey(self):
        return self.key

    def getLeftTree(self):
        return self.leftTree

    def getRightTree(self):
        return self.rightTree

    def insertLeft(self, key):
        if self.leftTree == None:
            self.leftTree = BinaryTree(key)

        else:
            t = BinaryTree(key)
            self.leftTree, t.leftTree = t, self.leftTree

    def insertRight(self, key):
        if self.rightTree == None:
            self.rightTree = BinaryTree(key)

        else:
            t = BinaryTree(key)
            self.rightTree, t.rightTree = t, self.rightTree

    def printPreorder(self, level):
        print(str(level * "~") + " " + str(self.key))

        if self.leftTree != None:
            self.leftTree.printPreorder(level + 1)

        if self.rightTree != None:
            self.rightTree.printPreorder(level + 1)


# * PARSE TREE
def buildParseTree(exp):
    tokens = exp.split()

    stack = Stack()
    tree = BinaryTree("?")
    stack.push(tree)

    currentTree = tree

    for t in tokens:
        if t == "(":
            currentTree.insertLeft("?")
            stack.push(currentTree)

            currentTree = currentTree.getLeftTree()
        elif t in ["+", "-", "*", "/"]:
            currentTree.setKey(t)
            currentTree.insertRight("?")
            stack.push(currentTree)

            currentTree = currentTree.getRightTree()
        elif t == ")":
            currentTree = stack.pop()
        elif t not in ["+", "-", "*", "/"]:
            currentTree.setKey(int(t))
            parent = stack.pop()

            currentTree = parent
        else:
            raise ValueError

    return tree

def evaluate(tree):
    leftTree = tree.getLeftTree()
    rightTree = tree.getRightTree()
    op = tree.getKey()

    if leftTree != None and rightTree != None:
        if op == "+":
            return evaluate(leftTree) + evaluate(rightTree)
        elif op == "-":
            return evaluate(leftTree) - evaluate(rightTree)
        elif op == "*":
            return evaluate(leftTree) * evaluate(rightTree)
        elif op == "/":
            return evaluate(leftTree) / evaluate(rightTree)

    else:
        return tree.getKey()


exp = input("Calulate: ")
tree = buildParseTree(exp)
tree.printPreorder(0)
print(f"The expression {exp} evaluates to {evaluate(tree)}")