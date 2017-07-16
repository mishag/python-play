import threading
from threading import Lock, Condition
from collections import deque

class ObjectPool(object):
    def __init__(self, construct, reset, limit=4):
        self._construct = construct
        self._reset = reset

        self._lock = Lock()
        self._cond_have_objects = Condition(self._lock)
        self._pool = deque()
        self._max_num_objects = limit
        self._num_objects = 0

    def get(self):
        with self._lock:
            if len(self._pool) != 0:
                return self._pool.pop()

            # no objects in the pool

            if self._num_objects < self._max_num_objects:
                obj = construct()
                self._num_objects += 1
                return obj

            # no objects left, but reached maximum
            while len(self._pool) == 0:
                self._cond_have_objects.wait()

            assert len(self._pool) > 0

            return self._pool.pop()

    def put(self, obj):
        self._reset(obj)
        with self._lock:
            self._pool.append(obj)
            self._cond_have_objects.notify()

    def _inc_num_objects(self):
        with self._lock:
            self._num_objects += 1
            return self._num_objects

    @property
    def num_objects(self):
        with self._lock:
            return self._num_objects
    @property
    def num_available_objects(self):
        with self._lock:
            return len(self._pool)
