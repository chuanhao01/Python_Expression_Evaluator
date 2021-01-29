
''' Implementing Merge Sort 

#* For now, just do a normal Merge Sort Algorithm 
# (https://www.geeksforgeeks.org/merge-sort/)
#TODO: Sort by: Value (ascending order), Expr. length (ascending order)
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


if __name__ == "__main__":
    arr = [12, 437, 12048, 865, 21568, 912684, 1, 0, 7, 2368]

    print("Original arr", arr)
    mergeSort(arr)
    print("Sorted arr", arr)
