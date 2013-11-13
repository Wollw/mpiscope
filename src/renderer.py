import pygame
import copy
import json
import random
import urllib2
import time
import threading
import sys
import numpy
from jobrect import JobRect
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

white = (255,255,255)
black = (0,0,0)
grey = (128,128,128)
darkgrey = (0x22,0x22,0x22)

class FetchThread(threading.Thread):
    def __init__(self, lock):
        threading.Thread.__init__(self)
        self.status = -1
        self.lock = lock
        self.jobs = []

    def run(self):
        while 1:
            print("fetching...")
            req  = urllib2.urlopen("http://sentinel.sdsc.edu/data/jobs/gordon")
            jsonStr = "".join(req.readlines())
            with self.lock:
                jobsold = self.jobs
                self.jobs = json.loads(jsonStr)["jobs"]
                self.jobs.sort(cmp = lambda x,y: cmp(y["walltime_req"],x["walltime_req"]))
                if jobsold != self.jobs:
                    print("new data")
            time.sleep(60)

def run(pyscope):
    # get a job's data for testing
    pyscope.processCount = comm.Get_size()
    pyscope.comm = comm
    pyscope.rank = rank
    pyscope.jobPositions = {}
    pyscope.log = lambda x: 20*numpy.log(x)/numpy.log(2)

    lock = threading.Lock()
    fetchThread = FetchThread(lock)
    fetchThread.start()

    lines = [pyscope.height - pyscope.log(x * 500000) for x in range(2,100)]

    # setup the screen id text
    fontObj = pygame.font.Font("freesansbold.ttf",12)
    textSurf = fontObj.render("%d"%rank, True, white, black)
    textRect = textSurf.get_rect()
    textRect.center = (25,25)

    # wait for job list to actually fill
    while 1:
        lock.acquire()
        if fetchThread.jobs != []:
            lock.release()
            break
        else:
            lock.release()

    # main render loop
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                comm.allgather(False)
                pygame.quit()
                exit(0)
        pyscope.screen.fill(darkgrey)


        # Draw each job rectangle
        lock.acquire()
        jobs = copy.deepcopy(fetchThread.jobs)
        lock.release()
        [pygame.draw.line(pyscope.screen, white, (0, y), (pyscope.width, y), 1) for y in lines]
        for j in jobs:
            if "walltime_used" in j:
                jobRect = JobRect(pyscope, j)
                pygame.draw.rect(pyscope.screen, grey, jobRect.reqRect.move(-pyscope.width * rank, 0))
                pygame.draw.rect(pyscope.screen, jobRect.color, jobRect.usedRect.move(-pyscope.width * rank, 0))

        pyscope.screen.blit(textSurf, textRect)

        # wait for other processes and then display
        #comm.barrier()
        if not all(comm.allgather(True)):
            pygame.quit()
            exit(0)
        pygame.display.flip()
