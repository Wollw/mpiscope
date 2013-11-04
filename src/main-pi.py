#!/usr/bin/env python2
import os
import pygame
import time
import random
import sys
import json

from Job import Job
from JobRect import JobRect

white = (255,255,255)
black = (0,0,0)

#
# encapsulates the pygame configuration and game logic
#
# based on an example from adafruit at:
# http://learn.adafruit.com/pi-video-output-using-pygame/pointing-pygame-to-the-framebuffer
#
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
        
        self.width, self.height = size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        print "Framebuffer size: %d x %d" % (size[0], size[1])
        self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
        # Clear the screen to start
        self.screen.fill((0, 0, 0))
        # Initialise font support
        pygame.font.init()
        # Render the screen
        pygame.display.update()
        # Hide cursor
        pygame.mouse.set_visible(False)

    def __del__(self):
        "Destructor to make sure pygame shuts down, etc."

    def run(self):
        # get a job's data for testing
        infile = open("data/dataV.json", 'r')
        jsonStr = infile.read()
        data = json.loads(jsonStr)["jobs"]

        # Create job rectangles
        jobs = [JobRect(self, Job(d)) for d in data]

        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            self.screen.fill(black)

            # Draw each job rectangle
            for j in jobs:
                pygame.draw.rect(self.screen, j.color, j.rect)
                pygame.draw.rect(self.screen, white, j.rect, 1)

            pygame.display.flip()

pyscope().run()