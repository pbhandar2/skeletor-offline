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

    def time_elapsed(self):
        divider = 0
        if (self.unit == "ns"):
            divider = 1000000000
        return (self.cur_time - self.start_time)/divider

    def time_diff(self, time1, time2):
        divider = 0
        if (self.unit == "ns"):
            divider = 1000000000
        return (time2 - time1)/divider



