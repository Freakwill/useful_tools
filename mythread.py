#!/usr/bin/env python3.4
# -*- coding:utf-8 -*-

import threading
import time
import collections

class strThread(threading.Thread):
    # Deprecated
    def __init__(self, statement='', globals_={}, locals_={}):
        if isinstance(statement, (tuple, list)):
            statement = '\n'.join(statement)
        super(strThread, self).__init__(target=exec, args=(statement, globals_, locals_))
        self.statement = statement
        self.globals = globals_
        self.locals = locals_


class ThreadList(collections.UserList):
    # list of threads
    def __init__(self, threads=[]):
        self.data = threads

    def __len__(self):
        return len(self.threads)

    def copy(self):
        import copy
        copythreads = copy.deepcopy(self.data)
        return ThreadList(copythreads)

    def run(self):
        # run the threads
        self.start()
        self.join()

    def start(self, daemon=False):
        # to start the threads
        for thread in self:
            thread.daemon = daemon
            thread.start()

    def join(self):
        # wating to finish the threads
        for thread in self:
            thread.join()

    @property
    def result(self):
        # get the return values of all threads
        return [thread.result if hasattr(thread, 'result') else None for thread in self]

    def __ior__(self, other):
        # thread <- thread list | thread
        if isinstance(other, threading.Thread):
            self.threads.append(other)
        else:
            self.threads.extend(other.threads)
        return self

    def __ror__(self, other):
        self.threads.append(other)
        return self

    def __or__(self, other):
        cpy = self.copy()
        cpy += other
        return cpy


class DemoThread(threading.Thread):
    def __init__(self, sleep_time=None, *args, **kwargs):
        super(DemoThread, self).__init__(*args, **kwargs)
        self.sleep_time = sleep_time

    def start(self):
        print('at %s, thread %s starts'%(time.ctime(), self))
        super(DemoThread, self).start()

    def join(self):
        super(DemoThread, self).join()
        print('at %s, thread %s stops'%(time.ctime(), self))

    def sleep(self):
        if self.sleep_time:
            time.sleep(self.sleep_time)

    def run(self):
        self.run()
        print('at %s, thread %s runs'%(time.ctime(), self))
        if self.demo:
            time.sleep()




if __name__ == "__main__":
    # def f(n=5):
    #     for k in range(n):
    #         time.sleep(1)
    #         print('at %s Hello world %d(%d) times'%(time.ctime(), n, k))

    #pyth = FuncThreadList(f, [(5,),(8,),(3,)])
    #pyth.append(f)
    #pyth.run()

    A = [[1, 2], [3,2], [6,2]]
    threads = ThreadList([DemoThread(target=lambda x:x.append(1), name='', args=(lst,), sleep_time=1) for lst in A])
    for t in threads:
        # t.setDaemon(True)
        t.start()
    threads.join()
