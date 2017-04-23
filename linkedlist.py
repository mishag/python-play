#!/Users/mgurvich/bbgithub/bqservices/venv/bin/python3


class Node():
    def __init__(self, val, parent):
        self.value = val
        self._next = None
        self._prev = None
        self.parent = parent

    def __repr__(self):
        return " [ val: {} ]".format(self.value)

    def is_orphan(self):
        return self.parent is None


class LinkedList():
    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    def __repr__(self):
        res = ""
        cur_node = self.head
        while cur_node is not None:
            res += "{} ".format(cur_node)
            if cur_node is not self.tail:
                res += "->"
            cur_node = cur_node._next

        return res

    def __iter__(self):
        cur_node = self.head
        while cur_node is not None:
            yield cur_node
            cur_node = cur_node._next

        raise StopIteration()

    def __len__(self):
        return self._size

    def pop_front(self):
        if self.head is None:
            return None

        res = self.head
        self.head = self.head._next
        self._size -= 1

        if self.head is None:
            assert self.tail is res
            self.tail = None
        else:
            self.head._prev = None

        assert self.head is not res
        res._next = None
        res._prev = None
        res.parent = None
        return res

    def pop_back(self):
        if self.tail is None:
            return None

        assert self.tail is not None

        res = self.tail
        self.tail = self.tail._prev
        self._size -= 1

        if self.tail is None:
            assert self.head is res
            self.head = None
        else:
            self.tail._next = None

        assert self.tail is not res
        res._next = None
        res._prev = None
        res.parent = None
        return res

    def push_front(self, val):
        node = Node(val, self)
        self._size += 1
        if self.head is None:
            self.head = node
            self.tail = node
            return

        head = self.head
        head._prev = node
        node._next = head
        self.head = node

    def push_back(self, val):
        node = Node(val, self)
        self._size += 1
        if self.head is None:
            self.head = node
            self.tail = node
            return

        tail_node = self.tail
        tail_node._next = node
        node._prev = tail_node
        self.tail = node

        assert self._size > 0

    def empty(self):
        return self.head is None

    def _find_with_prev(self, val):
        # return a pair (prev, cur) with cur pointing to the first node
        # containing val and prev is s.t. prev._next is cur
        # if cur is the initial element prev is going to be None
        # if no val is found, both prev and cur are None

        if self.empty():
            return (None, None)

        if self.head.value == val:
            return (None, self.head)

        assert self.head is not None

        prev = self.head
        cur = self.head._next

        while cur is not None:
            assert prev._next is cur
            if cur.value == val:
                return (prev, cur)

            prev = cur
            cur = cur._next

        return (None, None)

    def find(self, val):
        _, cur = self._find_with_prev(val)
        return cur

    def insert_before(self, node, val):

        if node is None:
            # insert in the end
            self.push_back(val)
            return self.tail

        assert node.parent is self

        if node is self.head:
            self.push_front(val)
            return self.head

        assert node._next is not None
        assert node._prev is not None

        new_node = Node(val, self)
        node._prev._next = new_node
        new_node._next = node
        new_node._prev = node._prev
        node._prev = new_node

        return new_node

    def insert_after(self, node, val):
        if node is None:
            # insert in the beginning
            self.push_front(val)
            return self.head

        assert node.parent is self

        if node is self.tail:
            self.push_back(val)
            return self.tail

        assert node._next is not None
        assert node._prev is not None

        new_node = Node(val, self)
        node._next._prev = new_node
        new_node._next = node._next
        node._next = new_node
        new_node._prev = node

        return new_node

    def clear(self):
        self.head = None
        self.tail = None

    def splice(self, node, other_list):
        # insert other list into this before node
        # if node is None, append other_list to the end of this
        # other_list is set to empty list

        assert node is None or node.parent is self

        self._size += len(other_list)

        if other_list.empty():
            return self.tail

        if node is self.head:
            other_list.tail._next = node
            node._prev = other_list.tail
            self.head = other_list.head
            other_list.clear()
            return self.head

        if node is None:

            if self.tail is None:
                self.head = other_list.head
                self.tail = other_list.tail
                other_list.clear()
                return self.head

            assert self.tail is not None

            other_list.head._prev = self.tail
            self.tail._next = other_list.head
            self.tail = other_list.tail
            to_ret = other_list.head
            other_list.clear()
            return to_ret

        assert node is not None
        assert node._prev is not None        # node is head was covered earlier

        node._prev._next = other_list.head
        other_list.head._prev = node._prev
        node._prev = other_list.tail
        other_list.tail._next = node
        to_ret = other_list.head
        other_list.clear()
        return to_ret

    def delete_node(self, node):
        if node is None:
            return None

        self._size -= 1

        if node._prev is not None:
            node._prev._next = node._next

        if node._next is not None:
            node._next._prev = node._prev

        if self.head is node:
            self.head = node._next

        if self.tail is node:
            self.tail = node._prev

        return node

    def delete_value(self, val):
        prev, cur = self._find_with_prev(val)
        if prev is None and cur is None:
            return

        assert cur.value == val
        to_del = cur

        # if there is only one element, both head and tail must be set
        # to None
        if self.head is self.tail:
            self.head = None
            self.tail = None
            self._size = 0
            return to_del

        assert self.head is not self.tail

        # if cur is first element in the list, head must be adjusted
        if prev is None:
            assert self.head is cur
            self.head = cur._next
            self.head._prev = None
            self._size -= 1
            return to_del

        assert prev is not None

        # if cur is last element in the list and not first
        # tail must be adjusted
        if cur._next is None:
            assert cur is self.tail
            self.tail = prev
            prev._next = None
            self._size -= 1
            return to_del

        # no adjustment for head nor tail is required
        assert cur._next is not None
        prev._next = cur._next
        cur._next._prev = prev
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
