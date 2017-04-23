import unittest
from linkedlist import LinkedList as LL


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
        self.assertTrue(x.empty())
        self.assertEqual(len(x), 0)
        self.assertIsNone(x.head)
        self.assertIsNone(x.tail)

        x.push_back(1)
        x.push_back(2)
        res = x.pop_front()
        self.assertEqual(res.value, 1)
        self.assertIsNone(res.parent)
        self.assertEqual(len(x), 1)
        self.assertTrue(not x.empty())
        self.assertEqual(x.head.value, 2)
        self.assertEqual(x.tail.value, 2)
