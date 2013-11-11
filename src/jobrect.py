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
        self.width  = int(job["ppn"]) * int(job["nodect"])
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
    width = jrect.width
    height = pyscope.log(height)
    if not job["job_id"] in pyscope.jobPositions:
        if pyscope.rank == 0:
            rand = random.randrange(0,pyscope.processCount * pyscope.width)
            [pyscope.comm.send(rand, dest=r, tag=1) for r in range(1, pyscope.processCount)]
        else:
            rand = pyscope.comm.recv(source=0, tag=1)
        pyscope.jobPositions[job["job_id"]] = rand
    posX = pyscope.jobPositions[job["job_id"]]
    posY = pyscope.height - height
    return pygame.Rect(posX * pyscope.processCount, posY, width, height)

