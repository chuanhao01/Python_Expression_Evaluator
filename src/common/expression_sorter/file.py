
'''
This Python File will deal with the File I/O required for the
Expression Sorting Section of the application.
'''

class File:
    @staticmethod
    def read(filename):
        file_input = []
        
        # Reading file input
        f = open(filename, 'r')
        for line in f:
            file_input.append(line.strip())
        f.close()

        return file_input

    @staticmethod
    def write(filename, file_output):
        f = open(filename, 'w')

        for line in file_output:
            f.write(line)

        f.close()