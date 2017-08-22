import unittest
from linkedlist import LinkedList as LL
from linkedlist import Node


class TestLinkedList(unittest.TestCase):
    def test_init(self):
        x = LL()
        self.assertIsNone(x.head)
        self.assertIsNone(x.tail)
        self.assertEqual(len(x), 0)
        self.assertTrue(x.empty())

    def test_push_back(self):
        x = LL()
        x.push_back(1)
        self.assertEqual(len(x), 1)
        head = x.head
        tail = x.tail
        self.assertIs(head, tail)
        self.assertEqual(head.value, 1)
        self.assertIs(head.parent, x)

        x.push_back(2)
        self.assertEqual(len(x), 2)
        self.assertEqual(x.head.value, 1)
        self.assertEqual(x.tail.value, 2)
        self.assertIs(x.tail.parent, x)
        self.assertIs(x.head.parent, x)

    def test_push_front(self):
        x = LL()
        x.push_front(1)
        self.assertEqual(len(x), 1)
        self.assertIs(x.head, x.tail)
        self.assertIs(x.head.value, 1)

        x.push_front(2)
        self.assertEqual(len(x), 2)
        self.assertEqual(x.head.value, 2)
        self.assertEqual(x.tail.value, 1)
        self.assertIs(x.head.parent, x)
        self.assertIs(x.tail.parent, x)

    def test_pop_front(self):
        x = LL()
        res = x.pop_front()
        self.assertIsNone(res)
        self.assertIsNone(x.head)
        self.assertIsNone(x.tail)
        self.assertEqual(len(x), 0)

        x.push_back(1)
        res = x.pop_front()
        self.assertEqual(res.value, 1)
        self.assertIsNone(res.parent)
        self.assertIsNone(res._next)
        self.assertIsNone(res._prev)
        self.assertTrue(x.empty())
        self.assertEqual(len(x), 0)
        self.assertIsNone(x.head)
        self.assertIsNone(x.tail)

        x.push_back(1)
        x.push_back(2)
        res = x.pop_front()
        self.assertEqual(res.value, 1)
        self.assertIsNone(res.parent)
        self.assertIsNone(res._next)
        self.assertIsNone(res._prev)
        self.assertEqual(len(x), 1)
        self.assertTrue(not x.empty())
        self.assertEqual(x.head.value, 2)
        self.assertEqual(x.tail.value, 2)

    def test_pop_back(self):
        x = LL()
        res = x.pop_back()
        self.assertIsNone(res)
        self.assertIsNone(x.head)
        self.assertIsNone(x.tail)
        self.assertEqual(len(x), 0)

        x.push_back(1)
        res = x.pop_back()
        self.assertEqual(res.value, 1)
        self.assertIsNone(res.parent)
        self.assertIsNone(res._next)
        self.assertIsNone(res._prev)
        self.assertTrue(x.empty())
        self.assertEqual(len(x), 0)
        self.assertIsNone(x.head)
        self.assertIsNone(x.tail)

        x.push_back(1)
        x.push_back(2)
        res = x.pop_back()
        self.assertEqual(res.value, 2)
        self.assertIsNone(res.parent)
        self.assertIsNone(res._next)
        self.assertIsNone(res._prev)
        self.assertEqual(len(x), 1)
        self.assertTrue(not x.empty())
        self.assertEqual(x.head.value, 1)
        self.assertEqual(x.tail.value, 1)

    def test_empty(self):
        x = LL()
        self.assertTrue(x.empty())
        x.push_back(3)
        self.assertTrue(not x.empty())

    def test_find(self):
        x = LL()
        res = x.find(0)
        self.assertIsNone(res)

        x.push_back(1)
        res = x.find(1)
        self.assertIsNotNone(res)
        self.assertEqual(res.value, 1)
        self.assertIs(res.parent, x)
        self.assertIsNone(res._next)
        self.assertIsNone(res._prev)

        x.push_back(2)
        x.push_back(1)

        res = x.find(1)
        self.assertIsNotNone(res)
        self.assertEqual(res.value, 1)
        self.assertIs(res.parent, x)
        self.assertIsNone(res._prev)
        self.assertEqual(res._next.value, 2)

        res = x.find(2)
        self.assertIsNotNone(res)
        self.assertEqual(res.value, 2)
        self.assertIs(res.parent, x)
        self.assertIsNotNone(res._prev)
        self.assertEqual(res._next.value, 1)

        x.push_back(3)
        res = x.find(3)
        self.assertIsNotNone(res)
        self.assertEqual(res.value, 3)
        self.assertIs(res.parent, x)
        self.assertIsNone(res._next)
        self.assertEqual(res._prev.value, 1)

        res = x.find(4)
        self.assertIsNone(res)

    def test_insert_before(self):
        x = LL()   # []
        x.insert_before(None, 1)
        self.assertEqual(len(x), 1)
        self.assertEqual(x.head.value, 1)
        self.assertEqual(x.tail.value, 1)

        # [ 1 ]

        node = x.find(1)
        res = x.insert_before(node, 2)
        self.assertEqual(res.value, 2)
        self.assertIsNone(res._prev)
        self.assertIs(res._next, node)
        self.assertIs(res.parent, x)
        self.assertIs(node._prev, res)
        self.assertIs(x.head, res)
        self.assertIs(x.tail, node)
        self.assertEqual(len(x), 2)

        # [ 2 1 ]

        node = x.find(1)
        res = x.insert_before(node, 3)
        self.assertEqual(res.value, 3)
        self.assertEqual(res._prev.value, 2)
        self.assertEqual(res._next.value, 1)
        self.assertIs(res._prev, x.head)
        self.assertIs(res._next, x.tail)
        self.assertIs(node._prev, res)
        self.assertIs(res.parent, x)
        self.assertEqual(len(x), 3)

        # [ 2 3 1 ]

        res = x.insert_before(None, 4)

        # [ 2 3 1 4 ]

        self.assertEqual(len(x), 4)
        self.assertEqual(x.tail.value, 4)
        self.assertEqual(res.value, 4)
        self.assertEqual(res._prev.value, 1)
        self.assertIsNone(res._next)
        self.assertIs(x.tail, res)

    def test_insert_after(self):
        x = LL()   # []
        x.insert_after(None, 1)
        self.assertEqual(len(x), 1)
        self.assertEqual(x.head.value, 1)
        self.assertEqual(x.tail.value, 1)

        # [ 1 ]

        node = x.find(1)
        res = x.insert_after(node, 2)
        # [ 1 2 ]
        self.assertEqual(res.value, 2)
        self.assertIsNone(res._next)
        self.assertIs(res._prev, node)
        self.assertIs(res.parent, x)
        self.assertIs(node._next, res)
        self.assertIs(x.head, node)
        self.assertIs(x.tail, res)
        self.assertEqual(len(x), 2)

        node = x.find(1)
        res = x.insert_after(node, 3)
        # [ 1 3 2 ]
        self.assertEqual(res.value, 3)
        self.assertEqual(res._prev.value, 1)
        self.assertEqual(res._next.value, 2)
        self.assertIs(res._prev, x.head)
        self.assertIs(res._next, x.tail)
        self.assertIs(node._next, res)
        self.assertIs(res.parent, x)
        self.assertEqual(len(x), 3)

        res = x.insert_after(None, 4)

        # [ 4 1 3 2 ]

        self.assertEqual(len(x), 4)
        self.assertEqual(x.tail.value, 2)
        self.assertEqual(x.head.value, 4)
        self.assertEqual(res.value, 4)
        self.assertEqual(res._next.value, 1)
        self.assertIsNone(res._prev)
        self.assertIs(res, x.head)

    def test_clear(self):
        x = LL()
        x.clear()
        self.assertEqual(len(x), 0)
        self.assertIsNone(x.head)
        self.assertIsNone(x.tail)

        x.push_back(1)
        x.push_back(2)
        x.clear()

        self.assertEqual(len(x), 0)
        self.assertIsNone(x.head)
        self.assertIsNone(x.tail)

    def test_iter(self):
        x = LL()

        for el in x:
            self.assertTrue(True)

        x.push_back(0)
        for i, el in enumerate(x):
            self.assertEqual(el.value, i)

        x.push_back(1)
        x.push_back(2)
        for i, el in enumerate(x):
            self.assertEqual(el.value, i)

    def test_splice(self):
        this = LL()
        other = LL()

        this.splice(other, None)
        self.assertIsNot(this, other)
        self.assertTrue(this.empty())
        self.assertTrue(other.empty())
        self.assertIsNone(this.head)
        self.assertIsNone(this.tail)
        self.assertIsNone(other.head)
        self.assertIsNone(other.tail)
        self.assertEqual(len(this), 0)
        self.assertEqual(len(other), 0)

        other.push_back(1)
        other.push_back(2)
        res = this.splice(other, None)
        self.assertEqual(res.value, 1)

        # this: [1, 2]
        # other: [ ]

        self.assertIsNone(other.head)
        self.assertIsNone(other.tail)
        self.assertTrue(other.empty())
        self.assertEqual(len(this), 2)
        self.assertEqual(this.head.value, 1)
        self.assertEqual(this.tail.value, 2)

        other.push_back(3)
        other.push_back(4)
        # this: [1, 2]
        # other: [3, 4]

        res = this.splice(other, None)
        self.assertEqual(res.value, 3)
        # this:  [1, 2, 3, 4]
        # other: []
        self.assertTrue(other.empty())
        self.assertIsNone(other.head)
        self.assertIsNone(other.tail)
        self.assertEqual(len(this), 4)
        self.assertEqual(this.head.value, 1)
        self.assertEqual(this.tail.value, 4)
        for i, el in enumerate(this):
            self.assertEqual(el.value, i+1)

        node = this.head
        other.push_back(-1)
        other.push_back(0)
        # this:  [1, 2, 3, 4]; node = [1]
        # other: [-1, 0]

        res = this.splice(other, node)
        self.assertEqual(res.value, -1)
        # this: [-1, 0, 1, 2, 3, 4]
        # other: []
        self.assertTrue(other.empty())
        self.assertIsNone(other.head)
        self.assertIsNone(other.tail)
        self.assertEqual(len(this), 6)
        self.assertEqual(this.head.value, -1)
        self.assertEqual(this.tail.value, 4)
        for i, el in enumerate(this):
            self.assertEqual(el.value, i - 1)

        this.clear()
        this.push_back(0)
        this.push_back(1)
        this.push_back(5)
        this.push_back(6)
        other.push_back(2)
        other.push_back(3)
        other.push_back(4)
        node = this.find(5)
        # this: [0 1 5 6]; node = [5]
        # other: [2 3 4]
        res = this.splice(other, node)
        self.assertEqual(res.value, 2)
        # this: [0 1 2 3 4 5 6]
        # other: []
        self.assertTrue(other.empty())
        self.assertIsNone(other.head)
        self.assertIsNone(other.tail)
        self.assertEqual(len(this), 7)
        self.assertEqual(this.head.value, 0)
        self.assertEqual(this.tail.value, 6)
        for i, el in enumerate(this):
            self.assertEqual(el.value, i)

    def test_delete_node(self):
        x = LL()
        res = x.delete_node(None)
        self.assertIsNone(res)
        self.assertIsNone(x.head)
        self.assertIsNone(x.tail)
        self.assertEqual(len(x), 0)

        x.push_back(1)
        node = x.find(1)
        res = x.delete_node(node)
        self.assertIs(res, node)
        self.assertEqual(res.value, 1)
        self.assertIsNone(x.head)
        self.assertIsNone(x.tail)
        self.assertEqual(len(x), 0)
        self.assertTrue(x.empty())
        self.assertIsNone(node.parent)
        self.assertIsNone(node._next)
        self.assertIsNone(node._prev)

        x.push_back(1)
        x.push_back(2)
        node = x.find(1)
        res = x.delete_node(node)
        self.assertIs(res, node)
        self.assertEqual(res.value, 1)
        self.assertEqual(x.head.value, 2)
        self.assertEqual(x.tail.value, 2)
        self.assertEqual(len(x), 1)
        self.assertIsNone(node.parent)
        self.assertIsNone(node._next)
        self.assertIsNone(node._prev)

        x.clear()
        x.push_back(1)
        x.push_back(2)
        x.push_back(3)
        node = x.find(2)
        res = x.delete_node(node)
        self.assertIs(res, node)
        self.assertEqual(res.value, 2)
        self.assertEqual(x.head.value, 1)
        self.assertEqual(x.tail.value, 3)
        self.assertEqual(len(x), 2)
        self.assertIsNone(node.parent)
        self.assertIsNone(node._next)
        self.assertIsNone(node._prev)
        self.assertIs(x.head._next, x.tail)
        self.assertIs(x.tail._prev, x.head)

        x.clear()
        x.push_back(1)
        x.push_back(2)
        node = x.find(2)
        res = x.delete_node(node)
        self.assertIs(res, node)
        self.assertEqual(res.value, 2)
        self.assertEqual(x.head.value, 1)
        self.assertEqual(x.tail.value, 1)
        self.assertEqual(len(x), 1)
        self.assertIsNone(node.parent)
        self.assertIsNone(node._next)
        self.assertIsNone(node._prev)

        node = Node(3)
        with self.assertRaises(ValueError):
            x.delete_node(node)

    def test_delete_value(self):
        pass
