def swap(lst, i, j):
    temp = lst[i]
    lst[i] = lst[j]
    lst[j] = temp


def _lexicographic_next(lst):
    if len(lst) == 1:
        return None

    # if len(lst) == 2:
    #     if lst[0] < lst[1]:
    #         return list(reversed(lst))
    #     else:
    #         return None

    new_tail = _lexicographic_next(lst[1:])
    head = lst[0]
    if new_tail is not None:
        new_tail.insert(0, head)
        return new_tail

    # new_tail is none
    temp_list = lst[:]
    head = temp_list[0]
    for i in range(len(temp_list) - 1, 0, -1):
        if temp_list[i] > head:
            swap(temp_list, i, 0)

            result = list(reversed(temp_list[1:]))
            result.insert(0, temp_list[0])
            return result

    return None


def _apply_cycle(cycle, X):
    if len(cycle) in (0, 1):
        return X

    temp = X[cycle[-1]]

    rcycle = tuple(reversed(cycle))
    for i, idx in enumerate(rcycle):
        if i == len(rcycle) - 1:
            break
        X[rcycle[i]] = X[rcycle[i+1]]

    X[cycle[0]] = temp

    return X


def permutations(dimension, start=None):
    if start is None:
        start = Permutation(dimension)

    if start.dim != dimension:
        raise ValueError("Dimensions must match")

    p = start
    while True:
        yield p
        lst = _lexicographic_next(p._repr)
        if lst is None:
            break
        p = Permutation.from_list(lst)


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

    def __eq__(self, other):
        return self._repr == other._repr

    def __ne__(self, other):
        return self._repr != other._repr

    def __str__(self):
        cycles = self.as_cycles()
        if len(cycles) == 0:
            return "()"

        return "".join(["{}".format(c) for c in cycles])

    def __repr__(self):
        return str(self)

    def as_cycles(self):
        elements = set(range(self.dim))
        cycle_list = []
        while len(elements) != 0:
            current_cycle = []
            el = elements.pop()
            current_cycle.append(el)
            current_element = self._repr[el]
            while current_element != current_cycle[0]:
                current_cycle.append(current_element)
                elements.remove(current_element)
                current_element = self._repr[current_element]

            if len(current_cycle) > 1:
                cycle_list.append(tuple(current_cycle))

        return cycle_list

    def act_on(self, X):
        cycles = self.as_cycles()
        for c in reversed(cycles):
            _apply_cycle(c, X)

        return X

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

    @staticmethod
    def from_cycle(cycle, dim):
        if max(cycle) >= dim:
            raise ValueError("Invalid cycle of dimension {}".format(dim))

        if len(set(cycle)) != len(cycle):
            raise ValueError("Cycle may not have duplicate elements")

        result = Permutation(dim)
        if len(cycle) == 1 or len(cycle) == 0:
            return result

        curr = cycle[0]
        succ = cycle[1]

        for i in range(len(cycle) - 1):
            curr = cycle[i]
            succ = cycle[i + 1]
            result._repr[curr] = succ

        result._repr[cycle[-1]] = cycle[0]

        return result

    @staticmethod
    def from_cycles(cycle_list, dim):
        result = Permutation(dim)
        for cycle in cycle_list:
            result = result * Permutation.from_cycle(cycle, dim)

        return result
