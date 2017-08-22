from object_pool import ObjectPool
from threading import Thread
from random import uniform
from multiprocessing.dummy import Pool as ThreadPool

import time
import unittest
import uuid


class X(object):
    def __init__(self):
        self._initialized = True
        self._uuid = str(uuid.uuid4())

    def use(self, duration=0):
        self._initialized = False
        time.sleep(duration)

    def reset(self):
        self._initialized = True

    @property
    def is_initialized(self):
        return self._initialized

    @property
    def uuid(self):
        return self._uuid


def _x_factory():
    return X()


def _x_resetter(x):
    x.reset()


class TestObjectPool(unittest.TestCase):
    def setUp(self):
        self._op = ObjectPool(construct=_x_factory, reset=_x_resetter)

    def test_pool_default_initialization(self):
        op = ObjectPool(_x_factory)
        self.assertEqual(op.num_objects, 0)
        self.assertEqual(op.num_available_objects, 0)
        self.assertEqual(op.max_num_objects, 4)

    def test_pool_initialization_with_reset_and_limit(self):
        op = ObjectPool(construct=_x_factory, reset=_x_resetter, limit=10)
        self.assertEqual(op.num_objects, 0)
        self.assertEqual(op.num_available_objects, 0)
        self.assertEqual(op.max_num_objects, 10)

    def test_get_and_put_item_without_resetter(self):
        op = ObjectPool(_x_factory)
        x = op.get()
        uuid = x.uuid
        self.assertIsInstance(x, X)
        self.assertTrue(x.is_initialized)
        self.assertEqual(op.num_available_objects, 0)
        self.assertEqual(op.num_objects, 1)
        self.assertEqual(op.max_num_objects, 4)
        x.use()
        self.assertFalse(x.is_initialized)
        op.put(x)
        self.assertEqual(op.num_available_objects, 1)
        self.assertEqual(op.num_objects, 1)
        self.assertEqual(op.max_num_objects, 4)
        y = op.get()
        self.assertEqual(uuid, y.uuid)  # y is what x was
        self.assertIsInstance(y, X)
        self.assertFalse(y.is_initialized)
        self.assertEqual(op.num_available_objects, 0)
        self.assertEqual(op.num_objects, 1)
        self.assertEqual(op.max_num_objects, 4)

    def test_get_and_put_item_with_resetter(self):
        x = self._op.get()
        uuid = x.uuid
        self.assertIsInstance(x, X)
        self.assertTrue(x.is_initialized)
        self.assertEqual(self._op.num_available_objects, 0)
        self.assertEqual(self._op.num_objects, 1)
        self.assertEqual(self._op.max_num_objects, 4)
        x.use()
        self.assertFalse(x.is_initialized)
        self._op.put(x)
        self.assertEqual(self._op.num_available_objects, 1)
        self.assertEqual(self._op.num_objects, 1)
        self.assertEqual(self._op.max_num_objects, 4)
        y = self._op.get()
        self.assertEqual(uuid, y.uuid)
        self.assertIsInstance(y, X)
        self.assertTrue(y.is_initialized)
        self.assertEqual(self._op.num_available_objects, 0)
        self.assertEqual(self._op.num_objects, 1)
        self.assertEqual(self._op.max_num_objects, 4)

    def test_get_max_num_objects(self):
        objects = []
        for i in range(self._op.max_num_objects):
            x = self._op.get()
            self.assertEqual(self._op.num_objects, i + 1)
            self.assertEqual(self._op.num_available_objects, 0)
            self.assertEqual(self._op.max_num_objects, 4)
            objects.append(x)

        for i, x in enumerate(objects):
            self._op.put(x)
            self.assertEqual(self._op.num_objects, 4)
            self.assertEqual(self._op.num_available_objects, i + 1)
            self.assertEqual(self._op.max_num_objects, 4)

    def test_block_when_pool_is_empty(self):

        def work(pool, duration):
            x = pool.get()
            x.use(duration)
            pool.put(x)

        # Use threads to exhaust the pool and hold on to the resources
        # for 2 seconds each
        threads = []
        for i in range(self._op.max_num_objects):
            t = Thread(target=work, args=(self._op, 2))
            threads.append(t)
            t.start()

        # Busy wait to make sure every thread has acquired its resource
        while(self._op.num_available_objects != 0):
            continue

        # Use main thread to try to acquire a resource, and measure time
        # it has to wait (which is around 2 seconds)
        start = time.time()
        x = self._op.get()
        wait_time = time.time() - start
        self.assertGreater(wait_time, 1.5)
        self.assertLess(wait_time, 2.5)
        self._op.put(x)

        for t in threads:
            t.join()

    def test_get_object_using_context_manager(self):

        with self._op.item() as x:
            self.assertTrue(x.is_initialized)
            x.use()
            self.assertFalse(x.is_initialized)
            self.assertEqual(self._op.num_available_objects, 0)
            self.assertEqual(self._op.num_objects, 1)

        self.assertEqual(self._op.num_available_objects, 1)
        self.assertEqual(self._op.num_objects, 1)
        y = self._op.get()
        self.assertTrue(y.is_initialized)
        self._op.put(y)

    def test_work_simulation(self):

        def work(duration):
            with self._op.item() as x:
                x.use(duration)

        work_items = [uniform(0, 0.1) for i in range(100)]

        # create some contention by having more threads than resources
        tp = ThreadPool(self._op.max_num_objects + 2)

        tp.map(work, work_items)
        self.assertEqual(self._op.num_objects, 4)
        self.assertEqual(self._op.num_available_objects, 4)

        # ensure all objects are in good state

        objects = []
        for i in range(self._op.max_num_objects):
            x = self._op.get()
            self.assertTrue(x.is_initialized)
            objects.append(x)

        self.assertEqual(self._op.num_available_objects, 0)
        self.assertEqual(len(objects), self._op.max_num_objects)
