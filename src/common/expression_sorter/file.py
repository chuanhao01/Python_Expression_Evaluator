
'''
This Python File will deal with the File I/O required for the
Expression Sorting Section of the application.
'''
from pathlib import Path
class File:
    @staticmethod
    def read(filename):
        file_input = []
        
        # Reading file input
        f = open(filename, 'r')
        for line in f:
            file_input.append([line.strip()])
        f.close()

        return file_input

    @staticmethod
    def write(filename, sortedList):
        f = open(filename, 'w+')
        for sublist in sortedList:
            value = sublist[0]
            f.write(f"*** Expressions with value = {value}\n")

            for expression in sublist[1]:
                #print(type(sublist[i]))
                f.write(f"{expression[0]} ==> {value}\n")

            f.write("\n")

        f.close()