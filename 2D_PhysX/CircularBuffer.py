import copy

class CircularBuffer(object):
    """Constant size buffer which overwrites its values cyclically"""

    def __init__(self, buffer_size=1):
        self.buffer_size = buffer_size
        self.list = buffer_size * [None]
        self.index = 0

    def __delete__(self):
        del self.index
        del self.list

    def val(self):
        return copy.copy(self.list[self.index])

    def push(self, value):
        self.index = (self.index + 1) % self.buffer_size
        self.list[self.index] = copy.copy(value)

    def pop(self):
        self.list[self.index] = None
        self.index = (self.index - 1) % self.buffer_size