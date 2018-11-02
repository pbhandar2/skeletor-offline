# coding=utf-8

"""
The I/O profiler that gives the users the I/O metrics.

Author: Pranav Bhandari <bhandaripranav94@gmail.com> 2018/11
"""

from traceReader.abstractReader import AbstractReader
import matplotlib.pyplot as plt
import math

func_map = {
    "float":  lambda x: float(x),
    "integer": lambda x: int(x),
    "string": lambda x: str(x)
}

class IOProfiler():

    def __init__(self, reader, block_size=-1):

        assert isinstance(reader, AbstractReader), \
            "This is not a valid reader: {}".format(reader)

        self.reader = reader
        self.data = {}
        self.min_max_data = {}
        self.block_data = {}
        self.length = -1
        self.block_size = block_size
        self.block_list = set([])
        self.start_time = -1

    def get_time_length(self):
        """
        Returns the length of the trace file.
        """
        if (self.length == -1):
            metric_calculator()

        return self.length

    def bucket_time(self, bucket_size):
        """
        Returns the time array with buckets of a given size 
        """
        if (self.length == -1):
            metric_calculator()

        bucket_diff = 1000000000 * bucket_size # readings are in nanosecond 
        start = self.data["time"][0]
        bucket_array = [start]
        for t in self.data["time"][1:]:
            diff = t - start
            multiplier = math.floor(diff/bucket_diff)
            final_time = start + multiplier * bucket_diff
            bucket_array.append(final_time)

        return bucket_array

    def get_access_data(self):
        print("This function should return the data needed to create the plot that we need. The data would have to be LBN vs Time but \
        would I also encode the read/write situation? What we would need is an array with [[array of time] [array of lbn] [array of R/W]]")

    def metric_calculator(self):
        """
        Calculates the metric of the file.
        """

        line = self.reader.get_next_line()
        start_time = -1
        count = 0

        while(line):

            line_data = self.get_line_data(line)
            self.update_data(line_data)

            # # the fields provided by the user
            # for field in self.reader.fields:
            #     field_object = self.reader.fields[field]
            #     field_type = field_object["type"]
            #     field_index = field_object["index"]
            #     line_array = line.split(self.reader.delimiter)

            #     if (field == "io_type"):
            #         field_value = self.process_io_type(line_array, field_index, field_object["values"])
            #     elif (field == "time"):
            #         cur_time = func_map[field_type](line_array[field_index])
            #         field_value = cur_time
            #         # record the start time
            #         if (start_time == -1):
            #             start_time = cur_time
            #     elif (field == "size"):
            #         field_value = func_map[field_type](line_array[field_index])
            #     elif (field == "block"):
            #         field_value = func_map[field_type](line_array[field_index])
            #         process_block(field_value, count)
            #     else:
            #         field_value = func_map[field_type](line_array[field_index])

            #     update_data(field, field_value, field_type)

            line = self.reader.get_next_line()

            count += 1

        self.length = cur_time - start_time
        print(self.min_max_data)
        bucks = self.bucket_time(5)

    def get_field_matrix(self, field, filename):
        """
            What I need to do is go through each offset value and get the indexes at which that offset values appears.
            After that create an array by putting 1 in where it was accessed and zero otherwise. Is there going to be a

        """

        # get the range of lbn numbers
        # get the time and create a matrix
        # how do I use the buckets here?
        range_lbn = self.min_max_data[field][1] - self.min_max_data[field][0]
        length = self.length

        # for i in range lbn values check the blocks dict and see when it is implemented 
        # I have the range for the time so I know how many to use 
        # binsize can tell me and give me value maybe, need to store the bins as well


    def update_data(self, line_data):
        for field in line_data:
            if (field == "io_type"):
                field_value = self.process_io_type(line_array, field_index, field_object["values"])
            elif (field == "time"):
                field_value = line_data[cur_time]
                if (self.start_time == -1):
                    self.start_time = field_value
            elif (field == "size"):
                field_value = line_data[cur_time]
            elif (field == "block"):
                field_value = line_data[cur_time]
                
    
    def get_line_data(self, line):
        line_data = {}
        for field in self.reader.fields:
            field_object = self.reader.fields[field]
            field_type = field_object["type"]
            field_index = field_object["index"]
            line_array = line.split(self.reader.delimiter)
            line_data[field] = func_map[field_type](line_array[field_index])

        return line_data




    def update_data(field, field_value, field_type):

        # if the field is in the data struct
        if field in self.data:
            self.data[field].append(field_value)
            min_max_array = self.min_max_data[field]
            if (field_type == "integer" or field_type == "float"):
                self.min_max_data[field] = [min(field_value, min_max_array[0]), max(field_value, min_max_array[1])]
        else:
            self.data[field] = [field_value]
            self.min_max_data[field] = [field_value, field_value]





    def plot_distribution(self, field, file_name, colorField=None, dpi=1200):
        """
        Plots the distribution of the given field over time.
        """
        print("Plot distribution of {}".format(field))
        plt.plot(self.data["time"], self.data[field])
        plt.xlabel("time")
        plt.ylabel(field)
        plt.title("time vs {}".format(field))
        plt.savefig(file_name, dpi=dpi)

    def plot_scatter(self, field, file_name, colorField=None, markerSize=1, binSize=0):
        """
        Saves a scatterplot of the given field.
        Params:
            field -- the field that is going to be plotted
            file_name -- the output file name
            colorField -- the field that will dictate the color of the points
            markerSize -- the size of the point
            binSize -- the size of the bins for time
        """
        print("Scatter plot of {}".format(field))

        colors = ["red", "gold", "darkgreen", "navy", "black"]

        color_map = {
            "read": "r",
            "write": "b"
        }
        color_array = [color_map[x] for x in self.data["io_type"]]

        if (binSize):
            time = self.bucket_time(binSize)
        else:
            time = self.data["time"]

        #print(len(set(time)))
        #print(len(self.data["time"]))
        #print(self.data["time"][:20])

        plt.scatter(time, self.data[field], color=color_array, s=markerSize, alpha=0.1)
        plt.xlabel("time")
        plt.ylabel(field)
        plt.ylim(0, max(self.data[field]))
        plt.title("time vs {}".format(field))
        plt.savefig(file_name, dpi=1200)

    def match_with_value(self, match_value, values):
        """
        Matches the value obtained from the trace with a predefined or user defined notation.
        E.g. 
            The library requires type of I/O to be under "io_type" in the 
            config dict and the read and write instances to be represented as "read" and "write"
            but some traces might have it as "R" and "W". The entry in the fields dictionary 
            would be:
            {
                ...,
                "fields": {
                    ...,
                    "io_type": {
                        "index": *index of the io_type value in the array seprated by delimiter
                        "type": *type of representation (might have 0 for read 1 for write or some string)*
                        "values": { *listing out the possible values*
                            "read": "R",
                            "write": "W"
                        }
                    }
                }
            } 

        Params:
            match_value -- value extracted from the trace for this field
            values -- the possible values for this field
        """

        for val in values:
            if(values[val] == match_value):
                return val
        raise Exception("The value {} is not a included in the fields object.".format(rw_value))

    def process_size(self, line_data):
        """
        Do proessing based on the value of the size
        """

        size = line_data["size"]



    def process_block(self, block, index):
        # need to update the dict with the value of time and also the index in time array 
        self.block_list.add(block)
        if block in self.block_data:
            self.block_data[block].append(index)
        else:
            self.block_data[block] = [index]






    
