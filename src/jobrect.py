#
# Representation of a Job as a rectangle to be rendered.
#
import hashlib
import random
import pygame

class JobRect:
    # Takes a Job to create a JobRect from
    def __init__(self, pyscope, job):
        self.state  = job["job_state"]
        self.color  = _hexColor(self.state, job["job_owner"])
        self.width  = int(int(job["ppn"]) * int(job["nodect"])) * pyscope.processCount
        self.height = int(job["walltime_req"])
        #self.posX = random.randrange(0,100)
        self.posX = int(hashlib.md5(job["job_id"]).hexdigest(), 16) % 100
        self.posY = 0
        self.rect = _jobRectToRect(pyscope, self)

# Create a hex color value from a value
def _hexColor(state, user):
    hexVal = int(hashlib.md5(user).hexdigest(), 16) % 0xffffff
    (r,g,b) = ( (hexVal >> 16) / 2.0
              , (hexVal >> 8 & 0xff) / 2.0
              , (hexVal & 0xff) / 2.0
              )
    if state == 'Q':
        return (r,g,b)
    elif state == 'R':
        return (r+128, g+128, b+128)
    else:
        return (0,0,0)

def _jobRectToRect(pyscope, jrect):
    width = jrect.width
    height = jrect.height / 500.0
    posX = (jrect.posX / 100.0) * pyscope.width + width / 2
    posY = jrect.posY + (pyscope.height / 2.0) - (height / 2.0)
    return pygame.Rect(posX * pyscope.processCount, posY, width, height)

