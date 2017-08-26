def _swap(lst, i, j):
    temp = lst[i]
    lst[i] = lst[j]
    lst[j] = temp


def _lexicographic_next(lst):
    if len(lst) == 1:
        return None

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
            _swap(temp_list, i, 0)

            result = list(reversed(temp_list[1:]))
            result.insert(0, temp_list[0])
            return result

    return None


def _subcycle_to_cycle(subcycle_string):
    result = []
    num_strings = subcycle_string.split(',')

    if len(num_strings) == 1:
        num_string = num_strings[0].strip()
        if not num_string:
            return tuple(result)

        num = int(num_string)
        result.append(num)
        return tuple(result)

    for num_string in num_strings:
        num_string = num_string.strip()
        if not num_string:
            raise ValueError("Invalid cycle string.")
        num = int(num_string)
        result.append(num)

    return tuple(result)


def _parse_cycle_string(cycle_string):
    # 1. find first '('
    # 2. find next ')'
    # 3. build cycle from the contained string
    # 4. move cursor past the ')'
    # 5. repeat

    if len(cycle_string) == 0:
        raise ValueError("Invalid permutation: {}".format(cycle_string))

    end_of_string = len(cycle_string)

    next_location = -1

    cycles = []

    while True:
        cur_location = next_location + 1
        if cur_location == end_of_string:
            break

        while (cur_location != end_of_string and
               cycle_string[cur_location] == ' '):
            cur_location += 1

        if cur_location == end_of_string:
            break

        if cycle_string[cur_location] != '(':
            raise ValueError("Expected '(' in the cycle string")

        next_location = cur_location
        while (next_location != end_of_string and
               cycle_string[next_location] != ')'):
            next_location += 1

        if next_location == end_of_string:
            raise ValueError("Expected a terminating ')' in the cycle string")

        sub_cycle_string = cycle_string[(cur_location + 1):next_location]
        subcycle = _subcycle_to_cycle(sub_cycle_string)

        cycles.append(subcycle)

    return cycles

    


def _apply_cycle(cycle, X):
    if len(cycle) in (0, 1):
        return X

    temp = X[cycle[-1]]

    rcycle = tuple(reversed(cycle))
    for i, _ in enumerate(rcycle):
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

    def __hash__(self):
        return hash(tuple(self._repr))

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

    def sign(self):
        cycles = self.as_cycles()
        current_sign = 1
        for c in cycles:
            factor = -1
            if len(c) in (0, 1) or len(c) % 2 == 1:
                factor = 1

            current_sign *= factor

        return current_sign

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
        if isinstance(cycle, tuple) and len(cycle) == 0:
            return Permutation(dim)

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

    @staticmethod
    def from_string(cycle_string, dim):
        cycles = _parse_cycle_string(cycle_string)
        return Permutation.from_cycles(cycles, dim)
