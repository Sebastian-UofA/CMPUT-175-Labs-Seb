class DLinkedListNode:
    # An instance of this class represents a node in Doubly-Linked List
    def __init__(self, initData, initNext, initPrevious):
        self.data = initData
        self.next = initNext
        self.previous = initPrevious

        if initNext != None:
            self.next.previous = self
        if initPrevious != None:
            self.previous.next = self

    def getData(self):
        return self.data

    def setData(self, newData):
        self.data = newData

    def getNext(self):
        return self.next

    def getPrevious(self):
        return self.previous

    def setNext(self, newNext):
        self.next = newNext

    def setPrevious(self, newPrevious):
        self.previous = newPrevious


class DLinkedList:
	# An instance of this class represents the Doubly-Linked List
	def __init__(self):
		# Constructor that takes no arguments and creates an empty list
		self.__head = None
		self.__tail = None
		self.__size= 0        

	def search(self, item):
		# method that takes an item to search and returns a boolean indicating if the item was found in the list or not.
		
		# set current to head of list 
		current = self.__head
		# initialize found to False
		found = False
		
		# loop over the list until item is found or end of list is reached
		while current != None and not found:
			if current.getData() == item: # item found, set found to True
				found= True
			else: # else move current to next node
				current = current.getNext()
		return found

	def index(self, item):
		# method that takes an item to search and returns the index of first occurrence of item in list if found, else return -1
		
		# set current to head of list
		current = self.__head
		# initialize found to False and index to 0
		found = False
		index = 0
		
		# loop over the list until item is found or end of list is reached
		while current != None and not found:
			if current.getData() == item: # item found, set found to True
				found= True
			else: # else move current to next node and increment index by 1
				current = current.getNext()
				index = index + 1
		if not found: # item not found, set index to -1
			index = -1
		return index    
  
	def add(self, item):
		# method that takes an item to insert and inserts the item at the start of list
        
		# create a new node with data=item, next=head and previous=None
		node = DLinkedListNode(item, self.__head, None)
		# not an empty list, update previous of head to node
		if self.__head != None:
			self.__head.setPrevious(node)
		else: # empty list, update tail to node
			self.__tail = node
		self.__head = node # update head to point to node
		self.__size = self.__size + 1 # increment size by 1
		
	def remove(self, item):
		# method that takes an item to remove and removes the first occurrence of the item from the list
        
		# set current to head node
		current = self.__head
		
		# loop over the list until the node with item is not found
		while current is not None and current.getData() != item:
			current = current.getNext()
		
		# item found
		if current is not None:
			# item is at head node
			if current == self.__head:
				self.__head = self.__head.getNext() # set head to next node
				if self.__head is not None: # list is not empty after removal
					self.__head.setPrevious(None) # update previous of head to none
				else: # list is empty after removal, update tail to none
					self.__tail = None
			elif current == self.__tail: # item is at tail node
				self.__tail = self.__tail.getPrevious() # move tail to previous node
				self.__tail.setNext(None) # update next of tail to None
			else: # item is at middle node
				# update next of node previous to current to node next to current
				current.getPrevious().setNext(current.getNext())
				# update previous of node next to current to node previous to current
				current.getNext().setPrevious(current.getPrevious())
				
			# update next and previous of current to None	
			current.setNext(None)
			current.setPrevious(None) 
			self.__size = self.__size - 1 # decrement size by 1
				
	def append(self, item):
        # method that takes an item and inserts it to the end of list
		
		# create a new node with data=item, next=None and previous=None
		node = DLinkedListNode(item, None, None)
		if self.__head == None: # empty list, update head to node
			self.__head = node
		else: # non-empty list
			self.__tail.setNext(node) # update next of tail to point to node
			node.setPrevious(self.__tail) # update previous of node to tail

		self.__tail = node # set tail to point to node
		self.__size = self.__size + 1 # increment size by 1
		
	def insert(self, pos, item):
		# method that takes an int for position and an item and inserts item at given position
		
		if pos == 0:
			self.add(item)
		elif pos == self.__size:
			self.append(item)
		else:
		
			# set current to head of list
			current = self.__head
			index = 0 # initialize index to 0
		
			while current != None and index != pos:
				current = current.getNext()
				index = index + 1
			
			if index == pos:
				# create a new node with data=item, next=None and previous=None
				node = DLinkedListNode(item, None, None)
				node.setNext(current)
				node.setPrevious(current.getPrevious())
				
				current.getPrevious().setNext(node)
				current.setPrevious(node)
				
				self.__size = self.__size + 1
	
	def pop1(self):
		# method that takes no arguments and removes and returns the last item from the list
		
		if self.__size == 0: # empty list, return None
			return None
		if self.__size == 1: # list contains one element
			# get the data of head
			element = self.__head.getData()
			# set head and tail to None
			self.__head = self.__tail = None
			self.__size = 0 # set size to 0
			return element
		
		# set element to data of tail
		element = self.__tail.getData()
		# update tail to node previous to tail
		self.__tail = self.__tail.getPrevious()
		# update next of tail to None
		self.__tail.setNext(None)
		self.__size	= self.__size - 1 # decrement size by 1
		return element # return element

	def pop(self, pos=None):
		# method that takes an integer for position and removes and returns the element at pos
		
		# pos argument not given, call pop1
		if pos is None:
			return self.pop1()
		
		# pos is less than 0 or greater than or equal to size of list, throw exception
		if pos < 0 or pos >= self.__size:
			raise Exception("Position outside the valid range")
			
		if pos == 0: # delete the head
			element = self.__head.getData() # set element to data of head
			self.__head = self.__head.getNext() # update head to node next to head
			if self.__head == None: # list is empty after removel, set tail to none
				self.__tail = None
			else: # else update previous of head to None
				self.__head.setPrevious(None)
			self.__size = self.__size - 1 # decrement size of list
			return element
		elif pos == self.__size	- 1:
			return self.pop1()
		
		# set current to head of list	
		current = self.__head
		# set index to 0
		index = 0
		
		# loop over the list to get the node at pos
		while current != None and index != pos:
			current = current.getNext()
			index = index + 1
			
		# get the data of current node	
		element = current.getData()
		# update next of node previous to current to node next to current
		current.getPrevious().setNext(current.getNext())
		# update previous of node next to current to node previous to current
		current.getNext().setPrevious(current.getPrevious())
		# set next and previous of current to None
		current.setNext(None)
		current.setPrevious(None)
		self.__size = self.__size - 1 # decrement size by 1
		return element
			
	def searchLarger(self, item):
		# method that takes an item and returns the index of first element which is larger than item, if found else return -1
		
		# set current to head of list
		current = self.__head
		index = 0 # set index to 0
		
		# loop over the list until the end or we reach a node with data greater than item
		while current != None and current.getData() <= item:
			current = current.getNext()
			index = index + 1
			
		# data greater than item not found, set index to -1
		if current is None:
			index = -1
		return index
		
	def getSize(self):
		# method that returns the number of elements in the list
		
		return self.__size
	
	def getItem(self, pos):
		# method that takes an integer for pos and returns the element at pos
		
		# pos is not negative
		if pos >= 0:
			index = 0 # set index to 0
			current = self.__head # set current to head of list
			
			# loop over the list until end or node at pos is reached
			while current != None and index != pos:
				current = current.getNext()
				index = index + 1
				
			if current is not None: # node at pos found
				return current.getData()
			else: # position outside range
				raise Exception("Position outside the valid range")	
				
		else: # pos is negative
			index = -1 # set index to -1
			current = self.__tail # set current to tail of list
			
			# loop over the list until the start of list is reached or we reach the node at pos
			while current != None and index != pos:
				current = current.getPrevious()
				index = index - 1
				
			if current is not None: # node at pos found
				return current.getData()
			else: # position outside range
				raise Exception("Position outside the valid range")
	
	def __str__(self):
		# method that returns a string containing the string representation of the list
		
		if self.__size == 0: # empty list, return empty string
			return ""
			
		current = self.__head # set current to head of list
		nodeList = "" # set nodeList to empty string
		
		# loop over the list until the last node is reached
		while current.getNext() is not None:
			nodeList = nodeList + "{} ".format(current.getData()) # append string representation of data followed by a space
			current = current.getNext()
			
		# append the last node's data to nodeList
		nodeList = nodeList + "{}".format(current.getData())
		return nodeList


def test():

    linked_list = DLinkedList()

    is_pass = (linked_list.getSize() == 0)
    assert is_pass == True, "fail the test"

    linked_list.add("World")
    linked_list.add("Hello")

    is_pass = (str(linked_list) == "Hello World")
    assert is_pass == True, "fail the test"

    is_pass = (linked_list.getSize() == 2)
    assert is_pass == True, "fail the test"

    is_pass = (linked_list.getItem(0) == "Hello")
    assert is_pass == True, "fail the test"

    is_pass = (linked_list.getItem(1) == "World")
    assert is_pass == True, "fail the test"

    is_pass = (linked_list.getItem(0) ==
               "Hello" and linked_list.getSize() == 2)
    assert is_pass == True, "fail the test"
    x = linked_list.pop(1)
    is_pass = (x == "World")
    assert is_pass == True, "fail the test"

    is_pass = (linked_list.pop() == "Hello")
    assert is_pass == True, "fail the test"

    is_pass = (linked_list.getSize() == 0)
    assert is_pass == True, "fail the test"

    int_list2 = DLinkedList()

    for i in range(0, 10):
        int_list2.add(i)
    int_list2.remove(1)
    int_list2.remove(3)
    int_list2.remove(2)
    int_list2.remove(0)
    is_pass = (str(int_list2) == "9 8 7 6 5 4")
    assert is_pass == True, "fail the test"

    for i in range(11, 13):
        int_list2.append(i)
    is_pass = (str(int_list2) == "9 8 7 6 5 4 11 12")
    assert is_pass == True, "fail the test"

    for i in range(21, 23):
        int_list2.insert(0, i)
    is_pass = (str(int_list2) == "22 21 9 8 7 6 5 4 11 12")
    assert is_pass == True, "fail the test"
    x = int_list2.getSize()
    is_pass = (int_list2.getSize() == 10)
    assert is_pass == True, "fail the test"

    int_list = DLinkedList()

    is_pass = (int_list.getSize() == 0)
    assert is_pass == True, "fail the test"

    for i in range(0, 1000):
        int_list.append(i)
    correctOrder = True

    is_pass = (int_list.getSize() == 1000)
    assert is_pass == True, "fail the test"

    for i in range(0, 200):
        if int_list.pop() != 999 - i:
            correctOrder = False

    is_pass = correctOrder
    assert is_pass == True, "fail the test"

    is_pass = (int_list.searchLarger(200) == 201)
    assert is_pass == True, "fail the test"

    int_list.insert(7, 801)
    x = int_list.searchLarger(800)
    is_pass = (int_list.searchLarger(800) == 7)
    assert is_pass == True, "fail the test"

    x = int_list.getItem(-1)
    is_pass = (int_list.getItem(-1) == 799)
    assert is_pass == True, "fail the test"

    is_pass = (int_list.getItem(-4) == 796)
    assert is_pass == True, "fail the test"

    if is_pass == True:
        print("=========== Congratulations! Your have finished exercise 2! ============")


if __name__ == '__main__':
    test()
