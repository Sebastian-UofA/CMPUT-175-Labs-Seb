#------Documentataion-unittest-python3--#
#Ref: https://docs.python.org/3/library/unittest.html
#Please follow the above website for the details of how unittest works.

'''
The unittest unit testing framework has a similar flavor as major unit testing frameworks in other languages. 
It supports test automation, sharing of setup and shutdown code for tests, aggregation of tests into collections, and
independence of the tests from the reporting framework.
'''

#The unittest module provides a rich set of tools for constructing and running tests. 
import unittest

from exercise_1 import *
import random

#'unittest' provides a base class, 'TestCase', which may be used to create new test cases.
#A testcase is created by subclassing unittest.TestCase. 
class TestEx1(unittest.TestCase):

    #The six individual tests are defined with methods whose names start with the letters test. 
    #This naming convention informs the test runner about which methods represent tests.
    def test_empty_array(self):
        input_array=[]
        recursive_selection_sort(input_array,0)
        '''
         we use one of the assert*() methods provided by the TestCase base class. 
         If the test fails, an exception will be raised with an explanatory message, and 
         unittest will identify the test case as a failure.
        '''
        self.assertEqual(input_array,[])
        
    def test_one_element(self):
        input_array=[0]
        recursive_selection_sort(input_array,1)
        self.assertEqual(input_array,[0])
        
    def test_in_and_out_of_order(self):
        input_array=[3,2,1]
        recursive_selection_sort(input_array,3)
        self.assertEqual(input_array,[3,2,1])
        
        input_array=[1,2,3]
        recursive_selection_sort(input_array,3)
        self.assertEqual(input_array,[3,2,1])
        
    def test_repeated_elements(self):
        input_array=[3,1,1,5]
        recursive_selection_sort(input_array,4)
        self.assertEqual(input_array,[5,3,1,1])
        
    def test_mixed_numbers(self):
        input_array=[2,-5,0,3,-2,4]
        recursive_selection_sort(input_array,6)
        self.assertEqual(input_array,[4,3,2,0,-2,-5])
        
    def test_random_numbers(self):
        input_array = [random.randint(1,1000) for i in range(500)]
        sorted_list = sorted(input_array, reverse=True)
        recursive_selection_sort(input_array,500)
        self.assertEqual(input_array,sorted_list)


if  __name__== "__main__":
    # unittest.main() provides a command-line interface to the test script.  
    unittest.main()
    '''When run from the command line, if all the tests passes, 
    then the above script produces an output that looks like this:
    ......
    ----------------------------------------------------------------------
    Ran 6 tests in ....s
    
    OK
    '''    

