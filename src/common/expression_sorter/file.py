
'''
This Python File will deal with the File I/O required for the
Expression Sorting Section of the application.
'''

class File:
    def __init__(self, filename):
        self.filename = filename
        self.file_input = []
        self.file_output = []

    def read(self):
        f = open(self.filename, 'r')

        for line in f:
            self.file_input.append(line.strip())

        f.close()


    def write(self):
        f = open(self.filename, 'w')

        for line in self.file_output:
            f.write(line)

        f.close()