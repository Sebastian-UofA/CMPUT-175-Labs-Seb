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
        self.__head = None
        self.__tail = None
        self.__size = 0

    def search(self, item):
        current = self.__head
        found = False

        while current != None and not found:
            if current.getData() == item:
                found = True

            else:
                current = current.getNext()

        return found

    def index(self, item):
        current = self.__head
        found = False
        index = 0

        while current != None and not found:
            if current.getData() == item:
                found = True

            else:
                current = current.getNext()
                index = index + 1

        if not found:
            index = -1

        return index

    def add(self, item):
        # adds the item to the start of the list
        new_node = DLinkedListNode(item, self.__head, None)
        if self.__head != None:
            self.__head.setPrevious(new_node)
        else:
            self.__tail = new_node
        self.__head = new_node
        self.__size += 1


    def remove(self, item):
        # Removes the first occurrence of the item in the list

        # Set current to head node
        current = self.__head 

        # Loop through the list until node with an item is found
        while current != None and current.getData() != item:
            current = current.getNext()

        if current != None:
            # Item is at head node
            if current == self.__head:
                self.__head = current.getNext()
                if self.__head != None: 
                    # List is not empty after removal
                    self.__head.setPrevious(None) 
                else: 
                    # List is empty after removal, update tail to None
                    self.__tail = None
            elif current == self.__tail: 
                # Item is at tail node
                self.__tail = self.__tail.getPrevious() 
                self.__tail.setNext(None) 
            else: 
                # Item is at a middle node
                current.getPrevious().setNext(current.getNext())
                current.getNext().setPrevious(current.getPrevious())

            # Update next and previous of current to None
            current.setNext(None)
            current.setPrevious(None)
            self.__size -= 1


    def append(self, item):
        # adds a new node to the tail of the list with item as its data
        node = DLinkedListNode(item, None, self.__tail)
        if self.__tail == None:
            self.__head = node
        else:
            self.__tail.setNext(node)
            node.setPrevious(self.__tail)

        self.__tail = node
        self.__size += 1

        
    def insert(self, pos, item):
        # method that takes an int for position and an item and inserts item at given position
        if pos == 0:
            self.add(item)
        elif pos == self.__size:
            self.append(item)
        else:
            # set current to head of list and index to 0
            current, index = self.__head, 0

            while current != None and index != pos:
                current = current.getNext()
                index += 1

            if index == pos:
                # create a new node with data=item, next=None and previous=None
                node = DLinkedListNode(item, None, None)
                node.setNext(current)
                node.setPrevious(current.getPrevious())

                current.getPrevious().setNext(node)
                current.setPrevious(node)

                self.__size += 1

    def pop1(self):
        # removes and returns the last item in the list
        if self.__head is None:  # empty list, return None
            return None
        if self.__size == 1:  # list contains only one item
            data = self.__head.getData()  # get the data of the head 
            self.__head = self.__tail = None  # set head and tail to None
            self.__size = 0 
            return data
        
        # set data to the data of the tail
        data = self.__tail.getData()
        self.__tail = self.__tail.getPrevious()
        self.__tail.setNext(None)
        self.__size -= 1
        return data

    def pop(self, pos=None):
        if pos is None:
            return self.pop1()

        if pos < 0 or pos >= self.__size:
            raise Exception("Position outside the valid range")

        if pos == 0:  # delete the head
            data = self.__head.getData()
            self.__head = self.__head.getNext()
            if self.__head is None:  # list is empty after removal
                self.__tail = None
            else:
                self.__head.setPrevious(None)
            self.__size -= 1
            return data

        if pos == self.__size - 1:
            return self.pop1()

        # set current to head of list and index to 0
        current, index = self.__head, 0

        # loop over the list to get the node at pos
        while current != None and index != pos:
            current = current.getNext()
            index += 1

        # get the data of current node
        data = current.getData()

        # update next of node previous to current to node next to current
        current.getPrevious().setNext(current.getNext())

        # update previous of node next to current to node previous to current
        current.getNext().setPrevious(current.getPrevious())

        # set next and previous of current to None
        current.setNext(None)
        current.setPrevious(None)

        self.__size -= 1  # decrement size by 1
        return data

    def searchLarger(self, item):
        # returns the position of the first occurrence of an item larger than the provided item
        # TODO
        current = self.__head
        index = 0
        while current != None:
            if current.getData() > item:
                return index
            index += 1
            current = current.getNext()
        return -1

    def getSize(self):
        return self.__size

    def getItem(self, pos):
        # returns the item at the given position.
        if pos < 0:
            pos = self.__size + pos

        if pos < 0 or pos >= self.__size:
            raise IndexError

        current = self.__head
        for _ in range(pos):
            current = current.getNext()

        return current.getData()

    def __str__(self):
        # create the string representation of the linked list
        current = self.__head
        result = ''
        while current != None:
            result += str(current.getData()) + " "
            current = current.getNext()
        return result.strip()


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
