Python Module: mpiscope
    Contains two user facing classes:
        mpiscope.MPIScope:

            https://github.com/Wollw/mpiscope/blob/master/mpiscope/MPIScope.py

            This is the main part of this module.  It is a class who's
            constructor takes a Renderer object and a list of URLs and
            optionally a delay time in seconds.  The Renderer is an object
            of a class that implements the same methods as the DummyRenderer
            discussed below and is what is used to provide the drawing
            and data parsing for data obtained by this class. The URL list
            is a dictionarl of URLs to query and are assumed to return a JSON
            string.  This data is stored as a dictionary using the same keys
            as the urlLIst but with a parsed JSON object instead of an url
            as the value.  The optional delay parameter is used to define
            the time between requests to the server for data; it defaults to
            sixty seconds.
            
            This class essentially abstracts away the threading and MPI
            usage required to obtain data and communicate between processes.
            It starts an UpdateThread that requests new data, runs the
            Renderer's provided parser method if defined, and shares it
            to other processes via MPI.  Meanwhile in the main thread, it
            runs a draw loop that calls the Renderer's draw function.

        mpiscope.DummyRenderer:

            https://github.com/Wollw/mpiscope/blob/master/mpiscope/DummyRenderer.py

            This is just a simple example Renderer class that does nothing.
            The methods of interest are start, parser, draw, and flip.

            The start method is called when the MPIScope object is told to
            start running; this is typically used for creating something like
            a new pygame window.  It is separate from __init__ so that a new
            window is not opened when the object is created, but only when
            it is time to start running the MPIScope.

            The parser method is used to transform the data into the format
            expected by the draw method.  This method is called on the
            UpdateThread in order to move this kind of computation off the
            main thread and free the main thread up for just rendering.

            The draw method is the heart of this class.  It is where
            data is turned into an image.
            
            The flip method is just whatever needs to be done to actually
            display the render buffer to the screen itself.  In pygame
            this is simply a call of pygame.display.flip() which displays
            the render buffer to the screen.
