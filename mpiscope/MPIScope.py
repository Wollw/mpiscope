"""
.. module:: mpiscope
   :synopsis: A module that provides classes for facilitating
              parallel graphics programs using MPI.

.. moduleauthor:: David E. Shere <david.e.shere@gmail.com>

"""
import copy
import json
import threading
import time
import urllib2

from mpi4py import MPI

class MPIScope:
    """Provides a scope for running a parallel graphics program.
    
    Although this class is intended for use in graphics programs
    it could be used for other purposes.  The renderer.draw method
    simply runs every tick if there is available data and
    renderer.flip runs every tick.

    """

    def __init__(self, renderer, urlList, parse=None, delay=60):
        """Initialize MPI and the _UpdateThread and store the renderer

        Args:
            renderer (Renderer): An object used to display fetched data.
            urlList ({str}): A dictionary of strings with names as keys.
            parse: this optional parameter should be a function that transforms
                   the fetched data from the servers into the format the
                   renderer expects.  This function runs on the UpdateThread
                   so it may be used to reduce the size of data before being
                   copied to the main thread.
            delay: The number of seconds to wait between data updates.
        """

        self.comm = MPI.COMM_WORLD
        self.rank = self.comm.Get_rank()
        self.renderer = renderer

        self.lock = threading.Lock()
        self.updateThread = _UpdateThread(self.lock, urlList, parse, delay)
        
    def run(self):
        """ Start up and run the renderer and updateThread.
        """
        self.updateThread.start()
        self.renderer.start()
        while 1:
            if self.updateThread.updated():
                with self.lock:
                    jobData = copy.deepcopy(self.updateThread.jobData)
            if jobData != None:
                self.renderer.draw(jobData)
            self.comm.barrier()
            self.renderer.flip()

class _UpdateThread(threading.Thread):
    """ This class is used to create a separate thread
        for fetching and presenting data that will be rendered.

    """

    def __init__(self, lock, urlList, parse=None, delay=60):
        """ Initialize the thread and prepare it for reading and
            storing the data from the urlList urls.

            Args:
                lock (Lock): Lock for maintaining thread safety.
                urlList ({str}): Dictionary of URLs to fetch data from.
            
            Kwargs:
                delay (int): The number of seconds to wait between fetches.

        """
        threading.Thread.__init__(self)
        self.status = -1
        self.lock = lock
        self.jobData = None
        self.urlList = urlList
        self.delay = delay
        self._updated = True
        self.comm = MPI.COMM_WORLD.Clone()
        self.parse = parse

    def run(self):
        """ Start fetching data from the urls.
        """

        """ Attempts to retrieve data from
            the server.  Retries several times
            if it fails, and then returns either
            the new data or None.
        """
        def retrieveData(url):
            jobData = {}
            tries = 3
            while tries:
                request = urllib2.urlopen(url)
                dataStr = "".join(request.readlines())
                jobData = json.loads(dataStr)
                if "jobs" in jobData:
                    return json.loads(dataStr)
                else:
                    tries = tries - 1
                    time.sleep(5)
            return None


        while 1:
            # Fetch and distribute data
            if self.comm.rank == 0:
                newJobData = { name: retrieveData(url)
                             for name, url
                             in self.urlList.iteritems()
                             }

                if self.parse != None:
                    newJobData = self.parse(newJobData)
            else:
                newJobData = None

            newJobData = self.comm.bcast(newJobData)

            # Store the new data
            with self.lock:
                oldData = self.jobData
                self.jobData = newJobData
                if self.jobData != oldData:
                    self._updated = True

            time.sleep(self.delay)

    """ Returns true if the data was updated;
        this resets to false when checked.
    """
    def updated(self):
        with self.lock:
            if self._updated:
                self._updated = False
                return True
            else:
                return False

