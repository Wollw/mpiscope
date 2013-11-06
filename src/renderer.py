import pygame
import json
import sys
from jobrect import JobRect
from job import Job

white = (255,255,255)
black = (0,0,0)

def run(pyscope):
    # get a job's data for testing
    infile = open("data/dataV.json", 'r')
    jsonStr = infile.read()
    data = json.loads(jsonStr)["jobs"]

    # Create job rectangles
    jobs = [JobRect(pyscope, Job(d)) for d in data]

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        pyscope.screen.fill(black)

        # Draw each job rectangle
        for j in jobs:
            pygame.draw.rect(pyscope.screen, j.color, j.rect)
            pygame.draw.rect(pyscope.screen, white, j.rect, 1)

        pygame.display.flip()
