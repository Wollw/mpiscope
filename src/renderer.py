import pygame
import json
import random
import urllib2
import time
import threading
import sys
from jobrect import JobRect
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

white = (255,255,255)
black = (0,0,0)

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
            jobsold = self.jobs
            with self.lock:
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

    lock = threading.Lock()
    thread = FetchThread(lock)
    thread.start()

    # Create job rectangles
    #jobRects = [JobRect(pyscope, j) for j in jobs]

    # setup the screen id text
    fontObj = pygame.font.Font("freesansbold.ttf",12)
    textSurf = fontObj.render("%d"%rank, True, white, black)
    textRect = textSurf.get_rect()
    textRect.center = (25,25)

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        pyscope.screen.fill(black)

        # Draw each job rectangle
        lock.acquire()
        jobs = thread.jobs
        lock.release()
        for j in jobs:
            if "walltime_used" in j:

                jobRect = JobRect(pyscope, j)
                pygame.draw.rect(pyscope.screen, (128,128,128), jobRect.reqRect.move(-pyscope.width * rank, 0))
                pygame.draw.rect(pyscope.screen, jobRect.color, jobRect.usedRect.move(-pyscope.width * rank, 0))

        pyscope.screen.blit(textSurf, textRect)

        # wait for other processes and then display
        pygame.display.flip()
