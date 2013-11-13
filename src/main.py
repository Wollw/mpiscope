#!/usr/bin/env python2
import copy
import json
import threading
import time
import urllib2

from mpi4py import MPI

from dummyrenderer import DummyRenderer

urlList = { "gordon"   : "http://sentinel.sdsc.edu/data/jobs/gordon"
          , "tscc"     : "http://sentinel.sdsc.edu/data/jobs/tscc"
          , "trestles" : "http://sentinel.sdsc.edu/data/jobs/trestles"
          }

class MPIScope:

    def __init__(self, renderer, urlList):
        self.comm = MPI.COMM_WORLD
        self.rank = self.comm.Get_rank()
        self.renderer = renderer

        self.lock = threading.Lock()
        self.updateThread = UpdateThread(self.lock, urlList)
        
    def run(self):
        self.updateThread.start()
        self.renderer.init()
        while 1:
            if self.updateThread.updated():
                with self.lock:
                    jobData = copy.deepcopy(self.updateThread.jobData)
            if jobData != None:
                self.renderer.draw(jobData)
            self.comm.barrier()
            self.renderer.flip()


class UpdateThread(threading.Thread):

    def __init__(self, lock, urlList, delay=60):
        threading.Thread.__init__(self)
        self.status = -1
        self.lock = lock
        self.jobData = None
        self.urlList = urlList
        self.delay = delay
        self._updated = True

    def run(self):
        while 1:
            requests = { name: urllib2.urlopen(url)
                       for name, url
                       in self.urlList.iteritems()
                       }

            jsonStrs = { name: "".join(req.readlines())
                       for name, req
                       in requests.iteritems()
                       }

            with self.lock:
                self.jobData = { name: json.loads(jstr)
                               for name, jstr
                               in jsonStrs.iteritems()
                            }
                self._updated = True
            time.sleep(self.delay)

    def updated(self):
        with self.lock:
            if self._updated:
                self._updated = False
                return True
            else:
                return False


if __name__ == "__main__":
    mpiScope = MPIScope(DummyRenderer(), urlList)
    mpiScope.run()
