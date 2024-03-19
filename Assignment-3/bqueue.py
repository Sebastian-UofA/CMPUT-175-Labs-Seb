class BoundedQueue:
    def __init__(self, capacity):
        self.queue = []
        self.capacity = capacity

    def is_full(self):
        return len(self.queue) == self.capacity

    def enqueue(self, item):
        if not self.is_full():
            self.queue.append(item)

    def dequeue(self):
        if not self.is_empty():
            return self.queue.pop(0)

    def is_empty(self):
        return len(self.queue) == 0
    
    def __len__(self):
        return len(self.queue) 

    def __repr__(self):
        return str(self.queue)
