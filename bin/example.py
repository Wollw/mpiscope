from mpiscope import MPIScope
from mpiscope import DummyRenderer

urlList = { "gordon"   : "http://sentinel.sdsc.edu/data/jobs/gordon"
          , "tscc"     : "http://sentinel.sdsc.edu/data/jobs/tscc"
          , "trestles" : "http://sentinel.sdsc.edu/data/jobs/trestles"
          }

#def parse(data):
#    return data
#mpiScope = MPIScope(DummyRenderer(), urlList, parse, delay=1)
mpiScope = MPIScope(DummyRenderer(), urlList)
mpiScope.run()
