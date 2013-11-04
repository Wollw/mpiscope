#
# Representation of a Job as a rectangle to be rendered.
#
import hashlib
import random
import pygame

class JobRect:
    # Takes a Job to create a JobRect from
    def __init__(self, pyscope, job):
        self.state  = job.state
        self.color  = _hexColor(job.owner)
        self.width  = int(job.core_count)
        self.height = int(job.wallrequest)
        self.posX = random.randrange(0,100)
        self.posY = 0
        self.rect = _jobRectToRect(pyscope, self)

# Create a hex color value from a value
def _hexColor(x):
    hexVal = int(hashlib.md5(x).hexdigest(), 16) % 0xffffff
    return ( hexVal >> 16
           , hexVal >> 8  & 0xff
           , hexVal       & 0xff
           )

def _jobRectToRect(pyscope, jrect):
    width = jrect.width
    height = jrect.height / 500.0
    posX = (jrect.posX / 100.0) * pyscope.width + width / 2
    posY = jrect.posY + (pyscope.height / 2.0) - (height / 2.0)
    return pygame.Rect(posX, posY, width, height)

