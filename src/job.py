# Eli Dai a11062387
# VIS 198  assignment 2

class Job:

    count = 0;

    def __init__(self, jobDict):
        self.name = jobDict["name"]
        self.qtime = jobDict["qtime"]
        self.queue = jobDict["queue"]
        self.state = jobDict["state"]
        self.wallrequest = jobDict["wallrequest"]
        self.starttime = jobDict["starttime"]
        self.mtime = jobDict["mtime"]
        self.owner = jobDict["owner"]
        self.node_count = jobDict["node_count"]
        self.id = jobDict["id"]
        self.core_count = jobDict["core_count"]
    
        self.color = "I don't know"
        self.size = "I don't konw"
    
    def displayJob(self):
        print "Name : ", self.name, ", qitme : ", self.qtime, ", queue : ", self.queue, ", state : ", self.state, ", wallrequest : ", self.wallrequest, self.color
        
        
#Job_1 = Job(1,2,3,4,5,6,7,8,9,10,11)
#Job_1.displayJob();
