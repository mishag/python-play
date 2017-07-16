from threading import Lock, Condition
from collections import deque


class ObjectPoolContextManager(object):
    def __init__(self, object_pool):
        self._op = object_pool
        self._obj = None

    def __enter__(self):
        self._obj = self._op.get()
        return self._obj

    def __exit__(self, exc_type, exc_value, traceback):
        self._op.put(self._obj)


class ObjectPool(object):
    def __init__(self, construct, reset=None, limit=4):
        self._construct = construct
        self._reset = reset

        self._lock = Lock()
        self._cond_have_objects = Condition(self._lock)
        self._pool = deque()
        self._max_num_objects = limit
        self._num_objects = 0

    def item(self):
        return ObjectPoolContextManager(self)

    def get(self):
        with self._lock:
            if len(self._pool) != 0:
                return self._pool.pop()

            # no objects in the pool

            if self._num_objects < self._max_num_objects:
                obj = self._construct()
                self._num_objects += 1
                return obj

            # no objects left, but reached maximum
            while len(self._pool) == 0:
                self._cond_have_objects.wait()

            assert len(self._pool) > 0

            return self._pool.pop()

    def put(self, obj):
        if self._reset is not None:
            self._reset(obj)

        with self._lock:
            self._pool.append(obj)
            self._cond_have_objects.notify()

    @property
    def num_objects(self):
        with self._lock:
            return self._num_objects

    @property
    def num_available_objects(self):
        with self._lock:
            return len(self._pool)
