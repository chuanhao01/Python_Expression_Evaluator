'''
This is the Python File containing the Sort class that
deals with sorting the various expressions from the input file

#* Features: Sort by Value, Length, Digit Order   ( Type )
#* Features: Sort by Ascending / Descending       ( Order )
'''

from .file import File

class Sort:
    def __init__(self, all_expr_list = None, sort_type = None, sort_order = None):
        self.__all_expr_list = all_expr_list
        self.__sort_type = sort_type
        self.__sort_order = sort_order

    def error(self):
        raise Exception("Error occurred while sorting..")


    #* Getter and Setter

    def get_all_expr_list(self):
        return self.__all_expr_list

    def set_all_expr_list(self, expr_list):
        self.__all_expr_list = expr_list

    def get_sort_type(self):
        return self.__sort_type

    def set_sort_type(self, sort_type):
        if sort_type not in ["value", "length", "digitOrder"]:
            self.error()

        self.__sort_type = sort_type
    
    def get_sort_order(self):
        return self.__sort_order

    def set_sort_order(self, sort_order):
        if sort_order not in ["ascending", "descending"]:
            self.error()

        self.__sort_order = sort_order

    #* 'Preprocessing' expression - get length of expression, remove whitespaces
    def preprocess_expr(self):
        all_expressions = self.get_all_expr_list()

        for expression in all_expressions:
            # Removing whitespaces
            expression[0] = expression[0].replace(" ", "")

            # Appending length of expression
            expression.append(len(str(expression[0])))

        return all_expressions

    #* Compile the sorted list into sublists based on value
    def compile_sortedList_by_value(self, sorted_exprList):
        value_list = [expression[1] for expression in sorted_exprList]
        expression_list = [expression for expression in sorted_exprList]
        
        unique_value_list = []
        for value in value_list:
            if value not in unique_value_list:
                unique_value_list.append(value)

        compiledList = []

        for i in range(0, len(unique_value_list)):
            value = unique_value_list[i]

            compiledList.append([value])
            compiledList[i].append([expression for expression in expression_list if expression[1] == value])

        return compiledList


    #* Sorting

    # 'Middleman' for mergeSort() method
    def sort(self):
        if self.get_sort_type() == "value":
            all_expressions = self.preprocess_expr()
        else:
            all_expressions = self.get_all_expr_list()

        sortedList = self.mergeSort(all_expressions)
        compiledList = self.compile_sortedList_by_value(sortedList)

        for sublist in compiledList:
            if len(sublist[1]) > 1:
                self.set_sort_type("length")
                sublist = self.mergeSort(sublist[1])

        return compiledList


    # Merge Sort WHEEEEEEEEE
    def mergeSort(self, expr_list):
        sort_order = self.get_sort_order()
        sort_type = self.get_sort_type()

        if sort_type == "value":
            list_index = 1
        elif sort_type == "length":
            list_index = 2

        if len(expr_list) > 1:
            #* Dividing the expr_list

            middleIndex = int(len(expr_list) / 2)

            # Splitting into left and right halves
            left_half = expr_list[:middleIndex]
            right_half = expr_list[middleIndex:]

            # Recursive call to continuously split the list into two halves
            self.mergeSort(left_half)
            self.mergeSort(right_half)

            left_index = right_index = merge_index = 0
            merge_list = expr_list


            #* Sorting && Merging

            while left_index < len(left_half) and right_index < len(right_half):
                if sort_order == "ascending":
                    if left_half[left_index][list_index] < right_half[right_index][list_index]:
                        merge_list[merge_index] = left_half[left_index]
                        left_index += 1

                    else:
                        merge_list[merge_index] = right_half[right_index]
                        right_index += 1

                elif sort_order == "descending":
                    if left_half[left_index][list_index] > right_half[right_index][list_index]:
                        merge_list[merge_index] = left_half[left_index]
                        left_index += 1

                    else:
                        merge_list[merge_index] = right_half[right_index]
                        right_index += 1

                else:
                    self.error()
                
                merge_index += 1

            # Handling any items still left in the left half of the list
            while left_index < len(left_half):
                merge_list[merge_index] = left_half[left_index]

                left_index += 1
                merge_index += 1

            # Handling any items still left in the right half of the list
            while right_index < len(right_half):
                merge_list[merge_index] = right_half[right_index]

                right_index += 1
                merge_index += 1

        return expr_list