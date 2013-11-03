#
# Representation of a Job as a rectangle to be rendered.
#
import hashlib
import random

class JobRect:
    # Takes a Job to create a JobRect from
    def __init__(self, job):
        self.state  = job.state
        self.color  = _hexColor(job.owner)
        self.width  = int(job.core_count)
        self.height = int(job.wallrequest)
        self.posX = random.randrange(0,100)
        self.posY = 0
        print(self.color)

# Create a hex color value from a value
def _hexColor(x):
    hex = int(hashlib.md5(x).hexdigest(), 16) % 0xffffff
    return ( hex >> 16
           , hex >> 8  & 0xff
           , hex       & 0xff
           )
