# Eli Dai a11062387
# VIS 198  assignment 2

import json
from Job import Job
fname = "data/dataV.json"
infile = open(fname,'r')
data = infile.read()
mydata = json.loads(data)

# experiment for initializing single object ---------------------------------

mylist = mydata["jobs"]

job1 = mylist[0]    # job1 or job2 or 3... are actually dictionaries.

print job1["name"]

print job1["qtime"]

print job1["queue"]

print job1["state"]

print job1["wallrequest"]

print job1["starttime"]

print job1["mtime"]

print job1["owner"]

print job1["node_count"]

print job1["id"]

print job1["core_count"]

job2 = mylist[1]

print job2["name"]

print len(mylist)  # this length tells the total number of job objects.

Job_1 = Job(job1)

Job_1.displayJob()
# succeed -----------------------------------------
