import random
import time

#---------------------------------------#      
# Implement Recursive selection sort here. 

# n: size of array - index is index of starting element
def recursive_selection_sort(data, data_len, index = 0):
    # Set the base case 
    # if the index is equal to the length of the data list, return (considered sorted)
    if index == data_len:
        return
    # Find the maximum index (since we are sorting in descending order) (acending order would be minimum index)
    max_index = index
    for i in range(index + 1, data_len):
        if data[i] > data[max_index]:
            max_index = i
    # Swap maximum value with the element at the current index (0 1 ....)
    data[index], data[max_index] = data[max_index], data[index]
    # Recursively calling selection sort function
    recursive_selection_sort(data, data_len, index + 1)
    

#---------------------------------------#
#Implement the Recursive merge sort here
  
def merge(left, right):
    # list to hold merged results
    result = []

    # while both left and right lists are not empty
    # compare the first element of the left and right lists
    # append the smaller element to the result list
    while left and right:
        if left[0] > right[0]:
            result.append(left.pop(0))
        else:
            result.append(right.pop(0))

    # At this point, either left or right is empty. Append the remainder of the non-empty list to result.
    result += left  # Appends the remaining elements of left, if any.
    result += right  # Appends the remaining elements of right, if any.
    return result

def recursive_merge_sort(data):
    # Set the base case
    # if the length of the data list is less than or equal to 1, return the data list
    if len(data) <= 1:
        return data
    
    # Find the middle of the data list
    middle = len(data) // 2
    # Recursively calling merge sort function for both half of the data list
    left = recursive_merge_sort(data[:middle])
    right = recursive_merge_sort(data[middle:])
    # merge the two halves of the data list and return the data list
    return merge(left, right)
     
#---------------------------------------#
if  __name__== "__main__":
    # Define the list of random numbers
    random_list = [random.randint(1,1000) for i in range(500)]
    list_len = len(random_list) 
    ascending_list = sorted(random_list)
    descending_list = sorted(random_list, reverse=True)
      
    # Calculate the execution time to sort a list of random numbers #
    random_list_ = random_list.copy()  # make a copy to save the unsorted list
    start_sel = time.time()
    recursive_selection_sort(random_list_, list_len)
    end_sel = time.time()
    
    start_merge = time.time()
    recursive_merge_sort(random_list)
    end_merge = time.time()
    
    # Print the rsults execution time to sort a list of random numbers
    print('The execution time: to sort a random list of integers in descending order.')
    print(' - Recursive selection sort: {}'.format(end_sel - start_sel))
    print(' - Recursive merge sort: {}'.format(end_merge - start_merge))
    
    
    # Calculate the execution time to sort a list of intergers already sorted in ascending order #
    ascending_list_ = ascending_list.copy()
    start_sel = time.time()
    recursive_selection_sort(ascending_list_, list_len)
    end_sel = time.time()
    
    start_merge = time.time()
    recursive_merge_sort(ascending_list)
    end_merge = time.time()
    
    # Print the rsults execution time to sort a list of intergers already sorted in ascending order 
    print('The execution time: to sort a ascending list of integers in descending order.')
    print(' - Recursive selection sort: {}'.format(end_sel - start_sel))
    print(' - Recursive merge sort: {}'.format(end_merge - start_merge))      
    
    
    # Calculate the execution time to sort a list of intergers already sorted in descending order #
    descending_list_ = descending_list.copy()
    start_sel = time.time()
    recursive_selection_sort(descending_list_, list_len)
    end_sel = time.time()
    
    start_merge = time.time()
    recursive_merge_sort(descending_list)
    end_merge = time.time()
    
    # Print the rsults execution time to sort a list of intergers already sorted in descending order 
    print('The execution time: to sort a descending list of integers in descending order.')
    print(' - Recursive selection sort: {}'.format(end_sel - start_sel))
    print(' - Recursive merge sort: {}'.format(end_merge - start_merge))
