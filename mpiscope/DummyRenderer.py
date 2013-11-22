"""
.. module:: dummyrenderer
   :synopsis: This module contains an example Renderer for MPIScope.

.. moduleauthor:: David E. Shere <david.e.shere@gmail.com>

"""

class DummyRenderer:
    """ This class is a mimimal implementation of a Renderer
        for MPIScope.
    """

    def __init__(self):
        """Any initialization goes here
        """
        return

    def start(self):
        """Do any further setup required to start rendering
           that wasn't done in __init__. This is a delayed initialization
           function so that things like a rendering window don't
           open when this class is instantiated, but only when run.
        """
        return

    def parse(self, data):
        """Do something to the data
        """
        return data

    def draw(self, jobData):
        """Do any drawing you want displayed.
           This method is only called when the
           UpdateThread actually has data (IE: is not None)
        """
        return

    def flip(self):
        """Do anything that needs to happen after drawing.
           This method is run every tick even if there is no data.
        """
        return
