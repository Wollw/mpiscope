#!/usr/bin/env python2
import pygame
import sys
import json

from Job import Job
from JobRect import JobRect

pygame.init()
width, height = 720, 480
size = width, height

# get a job's data for testing
infile = open("data/dataV.json", 'r')
jsonStr = infile.read()
data = json.loads(jsonStr)["jobs"]
jobrect = JobRect(Job(data[0]))

screen = pygame.display.set_mode(size)
rect = pygame.Rect( (jobrect.posX / 100.0) * width + jobrect.width / 2, 
                    jobrect.posY,
                    jobrect.width, jobrect.height)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    screen.fill((15,15,15))
    pygame.draw.rect(screen, jobrect.color, rect)
    pygame.display.flip()
