"""
.. module:: dummyrenderer
   :synopsis: This module contains an example Renderer for MPIScope.

.. moduleauthor:: David E. Shere <david.e.shere@gmail.com>

"""

class DummyRenderer:
    """ This class is a mimimal implementation of a Renderer
        for MPIScope.
    """

    def init(self):
        """Do any initialization required
        """
        print("init")

    def draw(self, jobData):
        """Do any drawing you want displayed.
           This method is only called when the
           UpdateThread actually has data (IE: is not None)
        """
        print("draw")

    def flip(self):
        """Do anything that needs to happen after drawing.
           This method is run every tick even if there is no data.
        """
        return
