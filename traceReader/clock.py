from traceReader.window_time_lib import filetime_to_dt

class clock():

    def __init__(self, _type):
        self.type = _type
        self.start_time = None 
        self.cur_time = None
        self.time_elasped = None 
        self.format = None 

    def get_time(self, time):

        if self.type == "windows":
            
            if not self.start_time:
                self.start_time = filetime_to_dt(time)

            self.cur_time = filetime_to_dt(time)
            self.time_elasped = self.cur_time - self.start_time

            # print("Current time is {}".format(self.cur_time))
            # print("Time time_elasped is {}".format(self.time_elasped))

        return self.cur_time

    def get_start_time(self):
        return self.start_time

    def get_cur_time(self):
        return self.cur_time

    def get_time_elasped(self):
        return self.time_elasped





