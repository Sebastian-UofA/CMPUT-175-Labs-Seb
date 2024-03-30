
import random
import time

def recursive_selection_sort(data, data_len, index=0):
    if index == data_len:
        return
    max_index = index
    for i in range(index + 1, data_len):
        if data[i] > data[max_index]:
            max_index = i
    data[index], data[max_index] = data[max_index], data[index]
    recursive_selection_sort(data, data_len, index + 1)

def merge(left, right):
    result = []
    while left and right:
        if left[0] > right[0]:
            result.append(left.pop(0))
        else:
            result.append(right.pop(0))
    result.extend(left or right)
    return result

def recursive_merge_sort(data):
    if len(data) <= 1:
        return data
    middle = len(data) // 2
    left = recursive_merge_sort(data[:middle])
    right = recursive_merge_sort(data[middle:])
    return merge(left, right)

if  __name__== "__main__":
    random_list = [random.randint(1,1000) for i in range(500)]
    list_len = len(random_list) 
    ascending_list = sorted(random_list)
    descending_list = sorted(random_list, reverse=True)
      
    random_list_ = random_list.copy()
    start_sel = time.time()
    recursive_selection_sort(random_list_, list_len)
    end_sel = time.time()
    
    start_merge = time.time()
    sorted_list = recursive_merge_sort(random_list)
    end_merge = time.time()
    
    print('The execution time: to sort a random list of integers in descending order.')
    print(' - Recursive selection sort: {}'.format(end_sel - start_sel))
    print(' - Recursive merge sort: {}'.format(end_merge - start_merge))
    
    ascending_list_ = ascending_list.copy()
    start_sel = time.time()
    recursive_selection_sort(ascending_list_, list_len)
    end_sel = time.time()
    
    start_merge = time.time()
    sorted_list = recursive_merge_sort(ascending_list)
    end_merge = time.time()
    
    print('The execution time: to sort a ascending list of integers in descending order.')
    print(' - Recursive selection sort: {}'.format(end_sel - start_sel))
    print(' - Recursive merge sort: {}'.format(end_merge - start_merge))      
    
    descending_list_ = descending_list.copy()
    start_sel = time.time()
    recursive_selection_sort(descending_list_, list_len)
    end_sel = time.time()
    
    start_merge = time.time()
    sorted_list = recursive_merge_sort(descending_list)
    end_merge = time.time()
    
    print('The execution time: to sort a descending list of integers in descending order.')
    print(' - Recursive selection sort: {}'.format(end_sel - start_sel))
    print(' - Recursive merge sort: {}'.format(end_merge - start_merge))
