class NanoTimeReader():

    def __init__(self):
    	self.unit = None
    	self.time_type = None
    	self.start_time = None
    	self.cur_time = None
    	self.format = None

    def update_time(self, time):
    	if not self.start_time:
    		self.start_time = time

    	self.cur_time = time

    def time_elapsed(self, time):
    	return self.cur_time - self.start_time

    def time_diff(self, time1, time2):
    	return time2 - time1
    	

