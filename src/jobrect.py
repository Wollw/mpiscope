#
# Representation of a Job as a rectangle to be rendered.
#
import hashlib
import random
import pygame
import numpy

class JobRect:
    # Takes a Job to create a JobRect from
    def __init__(self, pyscope, job):
        self.color  = _hexColor(job["job_owner"])
        self.width  = 8
        self.reqRect  = _jobRectToRect(pyscope, int(job["walltime_req"]), job, self)
        self.usedRect = _jobRectToRect(pyscope, int(job["walltime_used"]), job, self)

# Create a hex color value from a value
def _hexColor(user):
    hexVal = int(hashlib.md5(user).hexdigest(), 16) % 0xffffff
    (r,g,b) = ( (hexVal >> 16)
              , (hexVal >> 8 & 0xff)
              , (hexVal & 0xff)
              )
    return (r,g,b)

def _jobRectToRect(pyscope, height, job, jrect):
    global count
    rand = random.randrange(0,pyscope.processCount * pyscope.width)
    width = jrect.width
    height = pyscope.log(height)
    if not job["job_id"] in pyscope.jobPositions:
        pyscope.jobPositions[job["job_id"]] = pyscope.comm.allgather(rand)[0]
    posX = pyscope.jobPositions[job["job_id"]]
    posY = pyscope.height - height
    return pygame.Rect(posX * pyscope.processCount, posY, width, height)

