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
        print("Renderer Initialization")
        return

    def start(self):
        """Do any further setup required to start rendering
           that wasn't done in __init__. This is a delayed initialization
           function so that things like a rendering window don't
           open when this class is instantiated, but only when run.
        """
        print("Renderer Start")
        return

    def draw(self, data):
        """Do any drawing you want displayed.
           This method is only called when the
           UpdateThread actually has data (IE: is not None)
        """
        print("Renderer Draw")
        return

    def flip(self):
        """Do anything that needs to happen after drawing.
           This method is run every tick even if there is no data.
        """
        print("Renderer Flip")
        return
