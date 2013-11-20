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
        """Do any initialization required
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
