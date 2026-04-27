"""
queue.py — Implementasi Queue menggunakan Circular Array
Digunakan sebagai dasar untuk semua kasus implementasi.
"""


class Queue:
    """
    Queue berbasis circular array.
    Semua operasi: O(1)
    """

    def __init__(self, max_size=100):
        self._count = 0
        self._front = 0
        self._rear = max_size - 1
        self._data = [None] * max_size
        self._max_size = max_size

    def is_empty(self):
        return self._count == 0

    def is_full(self):
        return self._count == self._max_size

    def __len__(self):
        return self._count

    def enqueue(self, item):
        assert not self.is_full(), "Queue penuh!"
        self._rear = (self._rear + 1) % self._max_size
        self._data[self._rear] = item
        self._count += 1

    def dequeue(self):
        assert not self.is_empty(), "Queue kosong!"
        item = self._data[self._front]
        self._front = (self._front + 1) % self._max_size
        self._count -= 1
        return item

    def peek(self):
        assert not self.is_empty(), "Queue kosong!"
        return self._data[self._front]

    def __repr__(self):
        items = []
        for i in range(self._count):
            idx = (self._front + i) % self._max_size
            items.append(repr(self._data[idx]))
        return f"Queue([{', '.join(items)}])  # front → rear"
