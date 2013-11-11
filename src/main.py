#!/usr/bin/env python2
import pygame
import sys
import json
import renderer

from mpi4py import MPI

class PyScope:
    def __init__(self,width,height,screen):
        self.width = width
        self.height = height
        self.screen = screen

pygame.init()
width, height = 640, 480
size = width, height
screen = pygame.display.set_mode(size)
pyscope = PyScope(width, height, screen)

renderer.run(pyscope)
