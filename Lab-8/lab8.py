def mylen(some_list):
    '''
    This function takes a list as an argument and returns the length of the list. 0 if the list is empty.
    '''
    if not some_list:
        return 0
    else:
        return 1 + mylen(some_list[1:])
    
def intdivision(divident, divisor):
    '''
    This function takes two integers as arguments and returns the result of the division of the two integers.
    - isinstance(divident, int): This checks if the divident variable is an instance of the int class. It returns True if divident is an integer, and False otherwise.
    - divident < 0: This checks if the value of divident is less than 0. It returns True if divident is negative, and False otherwise.
    - divisor <= 0: This checks if the value of divisor is less than or equal to 0. It returns True if divisor is less than or equal to 0, and False otherwise.
    - raise ValueError("Invalid inputs. Dividend and divisor must be positive integers."): This raises a ValueError exception if the divident and/or divisor are not positive integers.
    If the divident is less than the divisor, the function returns 0.
    
    '''
    if not isinstance(divident, int) or not isinstance(divisor, int) or divident < 0 or divisor <= 0:
        raise ValueError("Invalid inputs. Dividend and divisor must be positive integers.")
    elif divident < divisor:
        return 0
    else:
        return 1 + intdivision(divident - divisor, divisor)
    
def sumDigits(some_num):
    '''
    This function takes an integer as an argument and returns the sum of its digits.
    if non integer or negative integer is entered, it raises a ValueError.
    '''
    if not isinstance(some_num, int) or some_num <= 0:
        raise ValueError("Invalid input. Number must be a positive integer.")
    elif len(str(some_num)) == 1:
        return some_num
    else:
        return some_num % 10 + sumDigits(some_num // 10)

def reverseDisplay(some_num):
    '''
    This function takes an integer as an argument and displays its digits in reverse order.
    if non integer or negative integer is entered, it raises a ValueError.
    '''
    if not isinstance(some_num, int) or some_num <= 0:
        raise ValueError("Invalid input. Number must be a positive integer.")
    else:
        some_num = str(some_num)
        if len(some_num) < 2:
            return int(some_num)
        else:
            return int(some_num[-1] + str(reverseDisplay(int(some_num[:-1]))))

def binary_search2(key, alist, low, high):
    '''
    - finds and returns the position of key in alist
    - or returns Item is not in the list
    - key is the target integer that we are looking for
    - alist is a list of valid integers that is searched
    - low is the lowest index of alist
    - high is the highest index of alist
    will return the index of the key in the list if found, otherwise it will return 'Item is not in the list'
    '''

    if low > high:
        return 'Item is not in the list'

    guess = (high + low) // 2 # find the middle index of the list

    if key == alist[guess]: # if the key is found, return the index
        return guess
    elif key < alist[guess]: # if the key is less than the value at the middle index, search the left half of the list
        return binary_search2(key, alist, low, guess - 1)
    else:                    # if the key is greater than the value at the middle index, search the right half of the list
        return binary_search2(key, alist, guess + 1, high)

def main():
    # Test the mylen function
    alist = [43,76,97,86]
    print(mylen(alist))

    # Test the intdivision function
    try:
        n = int(input("Enter an integer divident: "))
        m = int(input("Enter an integer divisor: "))
        print('Integer division', n, '//' , m, '=', intdivision(n, m))
    except ValueError as e:
        print("Error:", e)

    # Test the sumDigits function
    try:
        number = int(input('Enter a number: '))
        print(sumDigits(number))
    except ValueError as e:
        print("Error:", e)

    # Test the reverseDisplay function
    try:
        number = int(input('Enter a number: '))
        print(reverseDisplay(number))
    except ValueError as e:
        print("Error:", e)

    # Test the binary_search2 function
    some_list = [-8,-2,1,3,5,7,9]
    print()
    print(binary_search2(9,some_list,0,len(some_list)-1))
    print(binary_search2(-8,some_list,0,len(some_list)-1))
    print(binary_search2(4,some_list,0,len(some_list)-1)) # since 4 is not in the list, the search will eventually make low > high and return 'Item is not in the list'


main()
