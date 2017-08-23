import unittest
from permutation import Permutation, permutations


class TestPermutation(unittest.TestCase):
    def setUp(self):
        pass

    def test_default_construction(self):
        p = Permutation(3)
        self.assertEqual(p.dim, 3)
        self.assertEqual(p, Permutation.from_list([0, 1, 2]))
        for i in range(p.dim):
            self.assertEqual(p[i], i)

        q = Permutation(1)
        self.assertEqual(q.dim, 1)
        self.assertEqual(q, Permutation.from_list([0]))

    def test_construction_from_list(self):
        p = Permutation.from_list([0, 2, 1])
        self.assertEqual(p[0], 0)
        self.assertEqual(p[1], 2)
        self.assertEqual(p[2], 1)

    def test_construction_from_cycle(self):
        # mapping from (cycle, dim) -> list representation
        tests = {
            ((0,), 1): [0],
            ((1,), 4): [0, 1, 2, 3],
            ((1, 2), 4): [0, 2, 1, 3],
            ((0, 3), 4): [3, 1, 2, 0],
            ((0, 1, 2), 4): [1, 2, 0, 3],
            ((0, 3, 1), 4): [3, 0, 2, 1]
        }

        for test, result in tests.items():
            p = Permutation.from_cycle(test[0], test[1])
            self.assertEqual(p, Permutation.from_list(result))

    def test_exceptions_from_construction_from_cycle(self):
        with self.assertRaises(ValueError):
            Permutation.from_cycle((0, 1), 1)

        with self.assertRaises(ValueError):
            Permutation.from_cycle((4,), 4)

        with self.assertRaises(ValueError):
            Permutation.from_cycle((1, 2, 3, 1, 4), 5)

    def test_getitem(self):
        p = Permutation.from_list([1, 0, 2])
        self.assertEqual(p[0], 1)
        self.assertEqual(p[1], 0)
        self.assertEqual(p[2], 2)

    def test_equality(self):
        p = Permutation.from_list([1, 0, 2])
        q = Permutation.from_cycle((0, 1), 3)
        self.assertEqual(p, q)
        self.assertTrue(p == q)

        q = Permutation.from_cycle((0, 1), 2)
        self.assertNotEqual(p, q)
        self.assertTrue(p != q)

    def test_hash(self):
        p = Permutation.from_list([1, 0, 2])
        q = Permutation.from_cycle((0, 1), 3)
        self.assertEqual(p, q)
        self.assertEqual(hash(p), hash(q))

    def test_multiplication(self):
        tests = {
            ((0, 2, 1), (1, 2, 0)): [2, 1, 0],
            ((0, 1, 2), (1, 0, 2)): [1, 0, 2],
            ((1, 0, 2), (0, 1, 2)): [1, 0, 2],
            ((0, 2, 1), (2, 0, 1)): [1, 0, 2],
            ((2, 0, 1), (0, 2, 1)): [2, 1, 0],
            ((1, 0, 2), (1, 0, 2)): [0, 1, 2],
            ((1, 2, 0), (1, 2, 0)): [2, 0, 1]
        }

        for factors, expected in tests.items():
            left = Permutation.from_list(list(factors[0]))
            right = Permutation.from_list(list(factors[1]))
            result = left * right
            self.assertEqual(result, Permutation.from_list(expected))


class TestPermutationGenerator(unittest.TestCase):
    def test_generator_from_the_beginning(self):
        results = []
        for p in permutations(3):
            results.append(p)

        self.assertEqual(len(results), 6)
        self.assertEqual(results[0], Permutation.from_list([0, 1, 2]))
        self.assertEqual(results[1], Permutation.from_list([0, 2, 1]))
        self.assertEqual(results[2], Permutation.from_list([1, 0, 2]))
        self.assertEqual(results[3], Permutation.from_list([1, 2, 0]))
        self.assertEqual(results[4], Permutation.from_list([2, 0, 1]))
        self.assertEqual(results[5], Permutation.from_list([2, 1, 0]))

    def test_generator_with_custom_start(self):
        results = []
        for p in permutations(3, Permutation.from_list([1, 2, 0])):
            results.append(p)

        self.assertEqual(len(results), 3)
        self.assertEqual(results[0], Permutation.from_list([1, 2, 0]))
        self.assertEqual(results[1], Permutation.from_list([2, 0, 1]))
        self.assertEqual(results[2], Permutation.from_list([2, 1, 0]))
