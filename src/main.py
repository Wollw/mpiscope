#!/usr/bin/env python2
import copy
import json
import urllib2
import time

import threading
from threading import Thread
from mpi4py import MPI



url = "http://sentinel.sdsc.edu/data/jobs/gordon"


class MPIScope:

    def __init__(self, renderer):
        self.comm = MPI.COMM_WORLD
        self.rank = self.comm.Get_rank()
        self.renderer = renderer

        self.lock = threading.Lock()
        self.updateThread = UpdateThread(self.lock, url)
        
    def run(self):
        self.updateThread.start()
        self.renderer.init()
        while 1:
            with self.lock:
                jobData = copy.deepcopy(self.updateThread.jobData)
            if jobData != None:
                self.renderer.draw(jobData)
            self.comm.barrier()
            self.renderer.flip()


class UpdateThread(Thread):

    def __init__(self, lock, url, delay=60):
        Thread.__init__(self)
        self.status = -1
        self.lock = lock
        self.jobData = None
        self.jobDataUrl = url
        self.delay = delay

    def run(self):
        req = urllib2.urlopen(self.jobDataUrl)
        jsonStr = "".join(req.readlines())
        with self.lock:
            self.jobData = json.loads(jsonStr)
        time.sleep(self.delay)


class DummyRenderer:

    def init(self):
        print("init")

    def draw(self, jobData):
        print(jobData["jobs"][0])

    def flip(self):
        print("flip")

if __name__ == "__main__":
    mpiScope = MPIScope(DummyRenderer())
    mpiScope.run()
