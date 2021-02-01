'''
This is the Python File containing the Sort class that
deals with sorting the various expressions from the input file

#TODO: Sort by Value, Length, Digit Order   ( Type )
#TODO: Sort by Ascending / Descending       ( Order )
'''

from .file import File

class Sort:
    def __init__(self, expr_list, sort_type, sort_order):
        self.__expr_list = expr_list
        self.__sort_type = sort_type
        self.__sort_order = sort_order

    def error(self):
        raise Exception("Error occurred while sorting..")


    #* Getter and Setter

    def get_expr_list(self):
        return self.__expr_list

    def set_expr_list(self, expr_list):
        self.__expr_list = expr_list

    def get_sort_type(self):
        return self.__sort_type

    def set_sort_type(self, sort_type):
        self.__sort_type = sort_type
    
    def get_sort_order(self):
        return self.__sort_order

    def set_sort_order(self, sort_order):
        self.__sort_order = sort_order

    
    #* Sorting

    # Separating based on sort type - need preprocessing for some sort types
    def sort(self):
        sort_type = self.get_sort_type()

        sort_name = f"sort_by_{sort_type}"
        sort_method = getattr(self, sort_name, self.error)
        
        sort_method()

    # Preprocessing list before calling self.mergeSort()
    def sort_by_value(self):
        expr_list = self.get_expr_list()
        self.mergeSort(expr_list)

    def sort_by_length(self):
        expr_list = self.get_expr_list()
        pass

    def sort_by_digitOrder(self):
        pass

    # Merge Sort WHEEEEEEEEE
    def mergeSort(self, expr_list):
        sort_order = self.get_sort_order()

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
                    if left_half[left_index] < right_half[right_index]:
                        merge_list[merge_index] = left_half[left_index]
                        left_index += 1

                    else:
                        merge_list[merge_index] = right_half[right_index]
                        right_index += 1

                elif sort_order == "descending":
                    if left_half[left_index] > right_half[right_index]:
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

            print(expr_list)