from collections import deque


class _TrieNode(object):
    def __init__(self, char):
        self._char = char
        self._children = {}  # char -> TrieNode
        self._parent = None
        self._value = None
        self._terminal = False

    def __repr__(self):
        return ("[ [ char: {} ] "
                "[ terminal: {} ] "
                "[ value: {} ] "
                "[ children: {} ] ]".format(self._char,
                                            self._terminal,
                                            self._value,
                                            self._children.keys()))

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, val):
        self._parent = val

    @property
    def get_child(self, char):
        assert len(char) == 1
        return self._children.get(char)

    @property
    def has_child(self, char):
        assert len(char) == 1
        return char in self._children

    @property
    def is_terminal(self):
        return self._terminal

    def child_key_after(self, key_ord=0):
        if len(self._children) == 0:
            return None

        cur_min_ord = key_ord
        for child_key in self._children:
            child_key_ord = ord(child_key)
            if child_key_ord <= key_ord:
                continue

            if child_key_ord < cur_min_ord or cur_min_ord in (0, key_ord):
                cur_min_ord = child_key_ord

        assert cur_min_ord >= key_ord

        return None if cur_min_ord == key_ord else chr(cur_min_ord)


class TrieMap(object):
    def __init__(self):
        self._root = _TrieNode('')
        self._num_elements = 0

    def __len__(self):
        return self._num_elements

    def __getitem__(self, key):
        if len(key) == 0:
            raise KeyError("Key may not be empty")

        cur_node = self._root
        for c in key:
            cur_node = cur_node._children.get(c)
            if cur_node is None:
                raise KeyError("Key {} not found.".format(key))

        assert cur_node is not None
        assert cur_node._char == key[-1]

        if not cur_node.is_terminal:
            raise KeyError("Key {} not found.".format(key))

        return cur_node.value

    def __in__(self, key):
        if len(key) == 0:
            return False

        cur_node = self._root
        for c in key:
            cur_node = cur_node._children.get(c)
            if cur_node is None:
                return False

        return cur_node.is_terminal

    def _find_first_of(self, prefix=None):
        if prefix is None:
            return self._root

        cur_node = self._root
        for c in prefix:
            cur_node = cur_node._children.get(c)
            if cur_node is None:
                return None

        assert cur_node is not None
        return cur_node

    def _node_key(self, node):
        key = deque()
        while node is not self._root:
            key.appendleft(node._char)
            node = node.parent

        return ''.join(key)

    def _next_node(self, cur_node):
        if cur_node is self._root:
            if len(self._root._children) == 0:
                return None

            first_root_child_key = self._root.child_key_after(0)
            return self._root._children[first_root_child_key]

        if len(cur_node._children) != 0:
            first_child_key = cur_node.child_key_after(0)
            # print("First child key after 0 of node {} is {}"
            #       .format(cur_node, first_child_key))
            return cur_node._children[first_child_key]

        # Move up the tree until we have a next available child or until we
        # reach root node with no more children available for traversing.

        while True:
            cur_char = cur_node._char
            parent = cur_node.parent
            # get element in parent._children that follows cur_char
            next_child_key_in_parent = parent.child_key_after(ord(cur_char))
            if parent is self._root and next_child_key_in_parent is None:
                return None   # no next element

            if next_child_key_in_parent is None:
                cur_node = parent
                assert cur_node is not self._root
                continue

            # next child key in parent is not None
            return parent._children[next_child_key_in_parent]

    def __iter__(self):
        cur_node = self._root
        while cur_node is not None:
            if cur_node.is_terminal:
                yield self._node_key(cur_node)

            cur_node = self._next_node(cur_node)

    def items(self):
        cur_node = self._root
        while cur_node is not None:
            if cur_node.is_terminal:
                yield (self._node_key(cur_node), cur_node.value)

            cur_node = self._next_node(cur_node)

    def __str__(self):
        output = "{"
        for key, value in self.items():
            output += "{}: {}, ".format(key, value)
        output += "}"
        return output

    def __repr__(self):
        return str(self)

    def with_prefix(self, prefix=None):
        cur_node = self._find_first_of(prefix)
        if cur_node is None:
            return

        while cur_node is not None:
            if cur_node.is_terminal:
                yield (self._node_key(cur_node), cur_node.value)

            cur_node = self._next_node(cur_node)

    def __setitem__(self, key, value):
        if len(key) == 0:
            raise KeyError("Key may not be empty")

        cur_node = self._root
        for c in key:
            child = cur_node._children.get(c)
            if child is None:
                new_node = _TrieNode(c)
                new_node.parent = cur_node
                cur_node._children[c] = new_node
                cur_node = new_node
                continue

            cur_node = child

        if not cur_node._terminal:
            self._num_elements += 1

        cur_node._terminal = True
        cur_node.value = value
