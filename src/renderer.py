import pygame
import json
import urllib2
import sys
from jobrect import JobRect
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

white = (255,255,255)
black = (0,0,0)

def run(pyscope):
    # get a job's data for testing
    #infile = open("data/dataV.json", 'r')
    #jsonStr = infile.read()
    req  = urllib2.urlopen("http://sentinel.sdsc.edu/data/jobs/gordon")
    jsonStr = "".join(req.readlines())
    jobs = json.loads(jsonStr)["jobs"]
    pyscope.processCount = comm.Get_size()

    # Create job rectangles
    jobRects = [JobRect(pyscope, j) for j in jobs]

    # setup the screen id text
    fontObj = pygame.font.Font("freesansbold.ttf",12)
    textSurf = fontObj.render("%d"%rank, True, white, black)
    textRect = textSurf.get_rect()
    textRect.center = (25,25)

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                comm.allgather(False)
                print("quitting...")
                exit(0)
        pyscope.screen.fill(black)

        # Draw each job rectangle
        for j in jobRects:
            pygame.draw.rect(pyscope.screen, j.color, j.rect.move(-pyscope.width * rank, 0))
            pygame.draw.rect(pyscope.screen, white, j.rect.move(-pyscope.width * rank, 0), 1)

        pyscope.screen.blit(textSurf, textRect)

        # wait for other processes and then display
        flags = comm.allgather(True)
        if not(all(flags)):
            print("quitting...")
            exit(0)
        pygame.display.flip()
