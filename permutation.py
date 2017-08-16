class Permutation(object):
    def __init__(self, n_elements):
        self._repr = list(range(n_elements))

    @property
    def dim(self):
        return len(self._repr)

    def __getitem__(self, i):
        return self._repr[i]

    def __mul__(self, other):
        if not isinstance(other, Permutation):
            raise TypeError("Operands must be permutations")

        if self.dim != other.dim:
            raise TypeError("Permutation dimensions must be equal.")

        result = Permutation(self.dim)
        for i in range(self.dim):
            result._repr[i] = self[other[i]]

        return result

    def __str__(self):
        return "{}".format(self._repr)

    def __repr__(self):
        return str(self)

    @staticmethod
    def from_list(lst):
        if not isinstance(lst, list):
            raise TypeError("Cannot initialize from {}".format(lst))

        if len(set(lst)) != len(lst):
            raise ValueError("Cannot initialize permutation.")

        if min(lst) != 0 or max(lst) != len(lst) - 1:
            raise ValueError("Cannot initialize permutation")

        result = Permutation(len(lst))
        result._repr = lst
        return result
