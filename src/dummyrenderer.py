class DummyRenderer:

    def init(self):
        print("init")

    def draw(self, jobData):
        print(jobData.keys())

    def flip(self):
        return
