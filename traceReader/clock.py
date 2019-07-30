from traceReader.window_time_lib import filetime_to_dt
from datetime import datetime


class Clock():

    def __init__(self, _type, unit):
        self.type = _type
        self.start_time = None 
        self.cur_time = None
        self.time_elasped = None 
        self.format = None 
        self.unit = unit

    def get_time(self, time):

        if self.type == "windows":
            
            if not self.start_time:
                self.start_time = filetime_to_dt(time)

            self.cur_time = filetime_to_dt(time)

        elif self.type == "timestamp":

            if self.unit == "ns":
                if not self.start_time:
                    self.start_time = datetime.fromtimestamp(time // 1e9)

                self.cur_time = datetime.fromtimestamp(time // 1e9)

        elif self.type == "relative":

            if self.unit == "ns":
                if not self.start_time:
                    self.start_time = time // 1e9

                self.cur_time = time // 1e9

        self.time_elasped = self.cur_time - self.start_time

        return self.cur_time

    def get_start_time(self):
        return self.start_time

    def get_cur_time(self):
        return self.cur_time

    def get_time_elasped(self):
        return self.time_elasped

    def get_time_diff(self, time_value):
        if self.type == "relative":
            if self.unit == "ns":
                return (self.cur_time - time_value)//1e9
        elif self.type == "windows" or self.type == "timestamp":
            return (self.cur_time - time_value).total_seconds()







