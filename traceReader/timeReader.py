class TimeReader():

    def __init__(self, unit, time_type, time_format=None):
    	self.unit = unit
    	self.time_type = time_type
    	self.start_time = None
    	self.cur_time = None
    	self.format = time_format

    def update_time(self, time):
    	if not self.start_time:
    		self.start_time = time

    	self.cur_time = time

    def time_elapsed(self, time):
    	return self.cur_time - self.start_time

    def time_diff(self, time1, time2):
    	return time2 - time1


