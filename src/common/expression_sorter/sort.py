'''
This is the Python File containing the 'mergeSort' function

The function takes in only 1 argument, the list of expressions to be sorted

#TODO: This function still has to be adjusted to be able to sort by 2 values,
#TODO: The value of the evaluated expression and the Length of the expression (both in ascending order)
'''

def mergeSort(expr_list):
    if len(expr_list) > 1:
        #* Dividing the expr_list

        middleIndex = int(len(expr_list) / 2)

        # Splitting into left and right halves
        left_half = expr_list[:middleIndex]
        right_half = expr_list[middleIndex:]

        # Recursive call to continuously split the list into two halves
        mergeSort(left_half)
        mergeSort(right_half)

        left_index = right_index = merge_index = 0
        merge_list = expr_list


        #* Sorting && Merging

        while left_index < len(left_half) and right_index < len(right_half):
            if left_half[left_index] < right_half[right_index]:
                merge_list[merge_index] = left_half[left_index]
                left_index += 1

            else:
                merge_list[merge_index] = right_half[right_index]
                right_index += 1

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
