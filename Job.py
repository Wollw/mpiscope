# Eli Dai a11062387
# VIS 198  assignment 2

class Job:

	count = 0;

	def __init__(self, name, qtime, queue, state, wallrequest, starttime, mtime, owner, node_count, id, core_count):
		self.name = name;
		self.qtime = qtime;
		self.queue = queue;
		self.state = state;
		self.wallrequest = wallrequest;
		self.starttime = starttime;
		self.mtime = mtime;
		self.owner = owner;
		self.node_count = node_count;
		self.id = id;
		self.core_count = core_count;
	
		self.color = "I don't konw";
		self.size = "I don't konw";
	
	def displayJob(self):
		print "Name : ", self.name, ", qitme : ", self.qtime, ", queue : ", self.queue, ", state : ", self.state, ", wallrequest : ", self.wallrequest, self.color 
		
		
#Job_1 = Job(1,2,3,4,5,6,7,8,9,10,11)
#Job_1.displayJob();