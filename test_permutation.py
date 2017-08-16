import unittest
from permutation import Permutation, permutations


class TestPermutation(unittest.TestCase):
    def setUp(self):
        pass

    def test_default_initialization(self):
        p = Permutation(3)
        self.assertEqual(p.dim, 3)
        self.assertEqual(p, Permutation.from_list([0, 1, 2]))
        for i in range(p.dim):
            self.assertEqual(p[i], i)

        q = Permutation(1)
        self.assertEqual(q.dim, 1)
        self.assertEqual(q, Permutation.from_list([0]))

    def test_permutations_generator(self):
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
