#!/usr/bin/env python2
import os
import pygame
import time
import random
import sys
import json

from Job import Job
from JobRect import JobRect


# get a job's data for testing
infile = open("data/dataV.json", 'r')
jsonStr = infile.read()
data = json.loads(jsonStr)["jobs"]
jobrect = JobRect(Job(data[0]))


class pyscope :
    screen = None;
    
    def __init__(self):
        "Ininitializes a new pygame screen using the framebuffer"
        # Based on "Python GUI in Linux frame buffer"
        # http://www.karoltomala.com/blog/?p=679
        disp_no = os.getenv("DISPLAY")
        if disp_no:
            print "I'm running under X display = {0}".format(disp_no)
        
        # Check which frame buffer drivers are available
        # Start with fbcon since directfb hangs with composite output
        drivers = ['fbcon', 'directfb', 'svgalib']
        found = False
        for driver in drivers:
            # Make sure that SDL_VIDEODRIVER is set
            if not os.getenv('SDL_VIDEODRIVER'):
                os.putenv('SDL_VIDEODRIVER', driver)
            try:
                pygame.display.init()
            except pygame.error:
                print 'Driver: {0} failed.'.format(driver)
                continue
            found = True
            break
    
        if not found:
            raise Exception('No suitable video driver found!')
        
        width, height = size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        print "Framebuffer size: %d x %d" % (size[0], size[1])
        self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
        # Clear the screen to start
        self.screen.fill((0, 0, 0))
        # Initialise font support
        pygame.font.init()
        # Render the screen
        pygame.display.update()

        pygame.mouse.set_visible(False)

        self.rect = pygame.Rect(
                    ( jobrect.posX / 100.0) * width + jobrect.width / 2, 
                      jobrect.posY,
                      jobrect.width, jobrect.height)
 
    def __del__(self):
        "Destructor to make sure pygame shuts down, etc."

    def run(self):
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            self.screen.fill((50, 50, 50))
            pygame.draw.rect(self.screen, jobrect.color, self.rect)
            pygame.display.flip()

pyscope().run()
