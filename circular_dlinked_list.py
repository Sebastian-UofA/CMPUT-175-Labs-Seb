class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None  # Will be updated to point to the next node
        self.prev = None  # Will be updated to point to the previous node

    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data

    def get_next(self):
        return self.next

    def set_next(self, next_node):
        if not isinstance(next_node, Node) and next_node is not None:
            raise ValueError("next_node must be a Node instance or None")
        self.next = next_node

    def get_prev(self):
        return self.prev

    def set_prev(self, prev_node):
        if not isinstance(prev_node, Node) and prev_node is not None:
            raise ValueError("prev_node must be a Node instance or None")
        self.prev = prev_node


class CircularDoublyLinkedList:
    def __init__(self, capacity):
        self.head = None
        self.tail = None
        self.capacity = capacity
        self.size = 0

    def add_node(self, data):
        if self.size == self.capacity:
            raise Exception("List is at full capacity")
        new_node = Node(data)
        if self.head is None:
            self.head = self.tail = new_node
            new_node.next = new_node.prev = new_node
        else:
            new_node.prev = self.tail
            new_node.next = self.head
            self.tail.next = new_node
            self.head.prev = new_node
            self.tail = new_node
        self.size += 1

    def add_node_left(self, data):
        if self.size == self.capacity:
            raise Exception("List is at full capacity")
        new_node = Node(data)
        if self.head is None:
            self.head = self.tail = new_node
            new_node.next = new_node.prev = new_node
        else:
            new_node.prev = self.head.prev
            new_node.next = self.head
            self.head.prev.next = new_node  # Link the old predecessor to the new node
            self.head.prev = new_node  # Link the current head back to the new node
        self.head = new_node  # Make the new node the current node
        if self.head == 1:
            self.tail = new_node.next
        self.size += 1
        
    def add_node_right(self, data):
        if self.size == self.capacity:
            raise Exception("List is at full capacity")
        new_node = Node(data)
        if self.head is None:
            self.head = self.tail = new_node
            new_node.next = new_node.prev = new_node
        else:
            new_node.prev = self.head
            new_node.next = self.head.next
            self.head.next.prev = new_node  # Link the old successor's previous to new node
            self.head.next = new_node  # Link the current head's next to the new node
            if self.head == self.tail:  # If there was only one node before adding
                self.tail = new_node
        self.head = new_node    # Make the new node the current node
        self.size += 1


    def delete_current_node(self):
        if self.size == 0:
            raise Exception("The list is already empty.")
        elif self.size == 1:
            self.head = self.tail = None
        else:
            # If there are more than one nodes
            self.head.prev.next = self.head.next
            self.head.next.prev = self.head.prev
            self.head = self.head.next  # Move head to the next node
        self.size -= 1


    def get_current_node(self):
        if not self.head:
            raise Exception("List is empty")
        return self.head
    
    def get_size(self):
        return self.size

    def move_next(self):
        if not self.head:
            raise Exception("List is empty")
        self.head = self.head.next
        self.tail = self.tail.next

    def move_prev(self):
        if not self.head:
            raise Exception("List is empty")
        self.head = self.head.prev
        self.tail = self.tail.prev

