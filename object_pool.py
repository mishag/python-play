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
        self._num_objects = 0
        self._num_available_objects = 0

    def get(self):
        pass

    def put(self):
        pass

    def _inc_num_objects(self):
        with self._lock:
            self._num_objects += 1
            return self._num_objects

    def _inc_num_available_objects(self):
        with self._lock:
            self._num_available_objects += 1
            return self._num_available_objects

    def _dec_num_available_objects(self):
        with self._lock:
            self._num_available_objects -= 1
            return self._num_available_objects

    @property
    def num_objects(self):
        with self._lock:
            return self._num_objects
    @property
    def num_available_objects(self):
        with self._lock:
            return self._num_available_objects
