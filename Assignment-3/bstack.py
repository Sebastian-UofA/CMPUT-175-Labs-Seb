CHEMICAL_UNIT = 3  # Global constant for the chemical unit

class BoundedStack:
    def __init__(self, capacity=4):
        self.__items = []
        self.__capacity = capacity

    def initialize_stack(self, item):
        if len(self.__items) < self.__capacity:
            self.__items.append(item)
        # Do not seal the flask during initialization, even if it becomes full

    def push(self, item):
        if self.is_full():
            raise Exception("Stack is full, cannot add more items.")
        self.__items.append(item)

    def pop(self):
        if self.is_empty():
            raise Exception("Stack is empty, cannot pop an item.")
        return self.__items.pop()

    def peek(self):
        if self.is_empty():
            raise Exception("Cannot peek an empty stack.")
        return self.__items[len(self.__items) - 1]
    
    def get_item(self, index):
        return self.__items[index]
    
    def is_empty(self):
        return len(self.__items) == 0

    def is_full(self):
        return len(self.__items) == self.__capacity
    
    def size(self):
        return len(self.__items)
    
    def clear(self):
        self.__items = []

    def is_sealed(self):
        if len(self.__items) < CHEMICAL_UNIT:
            return False
        else:
            sealed_items = self.__items[-CHEMICAL_UNIT:]
            return all(item == sealed_items[0] for item in sealed_items)

    def __repr__(self):
        return "\n".join(["|{}|".format(item) for item in reversed(self.__items)] + ["+--+"])
    
    def __len__(self):
        return len(self.__items)  
