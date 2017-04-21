#!/Users/mgurvich/bbgithub/bqservices/venv/bin/python3


class Node():
    def __init__(self, val):
        self._val = val
        self._next = None
        self._size = 0

    def __repr__(self):
        return " [ val: {} ]".format(self._val)


class LinkedList():
    def __init__(self):
        self._head = None
        self._tail = None
        self._size = 0

    def __repr__(self):
        res = ""
        cur_node = self._head
        while cur_node is not None:
            res += "{} ".format(cur_node)
            cur_node = cur_node._next

        return res

    def __iter__(self):
        cur_node = self._head
        while cur_node is not None:
            yield cur_node
            cur_node = cur_node._next

        raise StopIteration()

    def __len__(self):
        return self._size

    def push_front(self, val):
        node = Node(val)
        self._size += 1
        if self._head is None:
            self._head = node
            self._tail = node
            return

        head = self._head
        node._next = head
        self._head = node

    def push_back(self, val):
        node = Node(val)
        self._size += 1
        if self._head is None:
            self._head = node
            self._tail = node
            return

        tail_node = self._tail
        tail_node._next = node
        self._tail = node

        assert self._size > 0

    def empty(self):
        return self._head is None

    def _find_with_prev(self, val):
        # return a pair (prev, cur) with cur pointing to the first node
        # containing val and prev is s.t. prev._next is cur
        # if cur is the initial element prev is going to be None
        # if no val is found, both prev and cur are None

        if self.empty():
            return (None, None)

        if self._head._val == val:
            return (None, self._head)

        assert self._head is not None

        prev = self._head
        cur = self._head._next

        while cur is not None:
            assert prev._next is cur
            if cur._val == val:
                return (prev, cur)

            prev = cur
            cur = cur._next

        return (None, None)

    def find(self, val):
        _, cur = self._find_with_prev(val)
        return cur

    def delete(self, val):
        prev, cur = self._find_with_prev(val)
        if prev is None and cur is None:
            return

        assert cur._val == val
        to_del = cur

        # if there is only one element, both head and tail must be set
        # to None
        if self._head is self._tail:
            self._head = None
            self._tail = None
            self._size = 0
            return to_del

        assert self._head is not self._tail

        # if cur is first element in the list, head must be adjusted
        if prev is None:
            assert self._head is cur
            self._head = cur._next
            self._size -= 1
            return to_del

        assert prev is not None

        # if cur is last element in the list and not first
        # tail must be adjusted
        if cur._next is None:
            assert cur is self._tail
            self._tail = prev
            prev._next = None
            self._size -= 1
            return to_del

        # no adjustment for head nor tail is required
        assert cur._next is not None
        prev._next = cur._next
        self._size -= 1
        return to_del


if __name__ == "__main__":
    l = LinkedList()
    l.push_back(1)
    print(l)
    l.push_back(2)
    print(l)

    print("Using iterators:")
    for x in l:
        print(x)
