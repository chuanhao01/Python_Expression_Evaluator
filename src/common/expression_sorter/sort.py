'''
This is the Python File containing the Sort class that
deals with sorting the various expressions from the input file

#TODO: Sort by Value, Length, Digit Order   ( Type )
#TODO: Sort by Ascending / Descending       ( Order )
'''

from file import File

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
        
        return sort_method()

    # Preprocessing list before calling self.mergeSort()
    def sort_by_value(self):
        expr_list = self.get_all_expr_list()

        return self.mergeSort(expr_list)

    def sort_by_length(self):
        expr_list = self.get_all_expr_list()

        for i in range(0, len(expr_list)):
            expr_list[i] = len(str(expr_list[i]))

        sorted_list = self.mergeSort(expr_list)
        
        #TODO: Figure out a way to link this back to the full expression
        return sorted_list

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

        return expr_list



if __name__ == "__main__":
    all_expressions = File.read(filename = './testCases.txt')

    #! Just evaluating all the expressions here for testing
    for i in range(0, len(all_expressions)):
        all_expressions[i] = eval(all_expressions[i])

    sort = Sort(all_expressions)

    print("Sort by Value in Ascending Order")
    sort.set_sort_order("ascending")
    sort.set_sort_type("value")
    print(sort.sort())

    print()

    print("Sort by Value in Descending Order")
    sort.set_sort_order("descending")
    sort.set_sort_type("value")
    print(sort.sort())   
    
    print()

    print("Sort by Length in Ascending Order")
    sort.set_sort_order("ascending")
    sort.set_sort_type("length")
    print(sort.sort())   
    
    print()

    print("Sort by Length in Descending Order")
    sort.set_sort_order("descending")
    sort.set_sort_type("length")
    print(sort.sort())   