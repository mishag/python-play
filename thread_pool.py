from collections import deque
import threading
from threading import Thread, Condition, Lock


def _dummy():
    return


class ThreadPoolError(Exception):
    def __init__(self, msg):
        self._msg = msg

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "ThreadPoolError: {}".format(self._msg)


class ThreadPool(object):

    RUNNING = 1
    STOPPING = 2
    STOPPED = 3

    def __init__(self, num_threads=4, queue_size=100):
        self._status = ThreadPool.STOPPED
        self._queue = deque()
        self._threads = {}   # thread id to thread
        self._lock = Lock()
        self._condition_not_full = Condition(self._lock)
        self._condition_not_empty = Condition(self._lock)
        self._max_queue_size = 100
        self._num_threads = num_threads

    @property
    def status(self):
        with self._lock:
            return self._status

    def _run(self):
        print("Thread {} starting to run"
              .format(threading.current_thread().name))

        while self.status != ThreadPool.STOPPED:
            with self._lock:

                while (len(self._queue) == 0 and
                       self._status != ThreadPool.STOPPED):

                    print("Thread {} waiting for jobs"
                          .format(threading.current_thread().name))
                    self._condition_not_empty.wait()

                if self._status == ThreadPool.STOPPED:
                    break

                assert len(self._queue) != 0

                job = self._queue.popleft()
                self._condition_not_full.notify()

                if (self._status == ThreadPool.STOPPING
                        and len(self._queue) == 0):
                    self._status = ThreadPool.STOPPED

            job()

        print("Stopping thread {}".format(threading.current_thread().name))

    def stop(self):
        if self.status in (ThreadPool.STOPPING, ThreadPool.STOPPED):
            return

        with self._lock:
            self._status = ThreadPool.STOPPING

            while self._status != ThreadPool.STOPPED:
                self._queue.append(_dummy)
                self._condition_not_empty.notify()

        for tid, t in self._threads:
            t.join()

    def start(self):
        with self._lock:
            if self._status == ThreadPool.RUNNING:
                return

            if self._status == ThreadPool.STOPPING:
                raise ThreadPoolError(
                    "Trying to start threadpool while it is stopping")

            self._status = ThreadPool.RUNNING
            self._threads = {}
            for i in range(self._num_threads):
                t = Thread(name=str(i), target=self._run)
                t.start()
                print("Started thread {}".format(t.name))
                self._threads[t.ident] = t

        print("Started")

    def submit(self, job):
        print("Submitting job")
        if self.status in (ThreadPool.STOPPING, ThreadPool.STOPPED):
            raise ThreadPoolError("Trying to submit jobs during pool shutdown")

        print("Acquiring lock")
        with self._lock:
            print("Acquired lock")
            while len(self._queue) == self._max_queue_size:
                self._condition_not_full.wait()

            assert len(self._queue) < self._max_queue_size

            print("Adding job to queue")
            self._queue.append(job)
            self._condition_not_empty.notify()
