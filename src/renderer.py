import pygame
import json
import sys
from jobrect import JobRect
from job import Job
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

white = (255,255,255)
black = (0,0,0)

def run(pyscope):
    # get a job's data for testing
    infile = open("data/dataV.json", 'r')
    jsonStr = infile.read()
    data = json.loads(jsonStr)["jobs"]
    
    pyscope.processCount = comm.Get_size()

    # Create job rectangles
    jobs = [JobRect(pyscope, Job(d)) for d in data]

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                comm.allgather(False)
                print("quitting...")
                exit(0)
        pyscope.screen.fill(black)

        # Draw each job rectangle
        for j in jobs:
            pygame.draw.rect(pyscope.screen, j.color, j.rect.move(-pyscope.width * rank, 0))
            pygame.draw.rect(pyscope.screen, white, j.rect.move(-pyscope.width * rank, 0), 1)

        # wait for other processes and then display
        flags = comm.allgather(True)
        if not(all(flags)):
            print("quitting...")
            exit(0)
        pygame.display.flip()
