# coding=utf-8

"""
The I/O profiler that gives the users the I/O metrics.

Author: Pranav Bhandari <bhandaripranav94@gmail.com> 2018/11
"""

from traceReader.abstractReader import AbstractReader
import matplotlib.pyplot as plt
import math
import collections

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
        self.block_data = collections.OrderedDict(reverse=True)
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
        count= 0;
        while(line):
            line_data = self.get_line_data(line)
            #print("Got line data for time {}".format(line_data["time"]))
            self.update_data(line_data)
            line = self.reader.get_next_line()


        self.length = self.data["time"][-1] - self.data["time"][0]
        print(self.min_max_data)
        print(self.length)

        for data_type in self.data:
            print("Info for {} len is {}".format(data_type, len(self.data[data_type])))

    def get_access_matrix(self, filename):
        print("Checkpoint 1")
        if (self.length == -1):
            metric_calculator()
        print("Checkpoint 2")

        for k,v in self.block_data.items():
            print(k)
        # [min_block, max_block] = self.min_max_data["block"]
        # f = open(filename, "w+")
        # print("Checkpoint 3")

        # """
        #     for key in sorted(self.block_data.keys(), reverse=True)
        # """

        # for i in range(max_block, min_block - 1, -1):
        #     if i in self.block_list:
        #         print(i)
        #         block_data = self.block_data[i]
        #         f.write(" ".join(self.get_access_matrix_row(block_data)))
        #         f.write("\n")

    def get_access_matrix_row(self, index):
        row = [0] * len(self.data["access_time"])
        for i in index:
            row[i] += 1
        return row

    def update_data(self, line_data):
        #print("The line data is {}".format(line_data))
        for field in line_data:
            #print("Updating field: {}".format(field))
            field_object = self.reader.fields[field]
            if (field == "io_type"):
                field_value = self.match_with_value(line_data[field], field_object["values"])
                self.update_field(field, field_value, "append")
            elif (field == "time"):
                field_value = line_data[field]
                self.update_field(field, field_value, "append")
                self.update_field("access_time", field_value, "append")
                if (self.start_time == -1):
                    self.start_time = field_value
            elif (field == "size"):
                field_value = line_data[field]
                self.update_field(field, field_value, "append")
                if (self.reader.block_size > 0):
                    self.process_size(line_data)
            elif (field == "block"):
                field_value = line_data[field]
                self.update_field(field, field_value, "append")
                self.process_block(field_value, len(self.data["access_time"]))
            else:
                field_value = line_data[field]
                self.update_field(field, field_value, "append")

        #print("Finished updating the data!")

    def get_line_data(self, line):
        line_data = {}
        for field in self.reader.fields:
            field_object = self.reader.fields[field]
            field_type = field_object["type"]
            field_index = field_object["index"]
            line_array = line.split(self.reader.delimiter)
            line_data[field] = func_map[field_type](line_array[field_index])

        return line_data

    def update_field(self, field, field_value, update_type):

        # if the field is in the data struct
        if field in self.data:
            if (update_type == "append"):
                self.data[field].append(field_value)
            elif (update_type == "add"):
                self.data[field] += 1
            else:
                raise ValueError("The value provided as update_type does not exist.")
        else:
            if (update_type == "append"):
                self.data[field] = [field_value]
            elif (update_type == "add"):
                self.data[field] = 1
            else:
                raise ValueError("The value provided as update_type does not exist.")

        # if it is a numeric or float value extract the min and max for it 
        if (isinstance(field_value, int) or isinstance(field_value, float)):
            min_max_array = self.min_max_data
            if field in min_max_array:
                self.min_max_data[field] = [min(field_value, min_max_array[field][0]), max(field_value, min_max_array[field][1])]
            else:
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
        Do proessing based on the value of the size in line data.
        Params:
            line_data -- all relevant data for the given line. 
        """
        

        size = line_data["size"]
        block_size = self.reader.block_size
        block = line_data["block"]
        cur_block = block + block_size

        #print("Processing size started for size {} and block {}".format(size, cur_block))

        while(cur_block < block+size):
            self.update_field("access_time", line_data["time"], "append")
            #print("Updated Access Time.")
            self.update_field("block", cur_block, "append")
            self.process_block(cur_block, len(self.data["access_time"]))
            cur_block += block_size

        #print("Processing size completed.")


    def process_block(self, block, index):
        # print("Processing the block {}".format(block))
        # need to update the dict with the value of time and also the index in time array 
        self.block_list.add(str(block))
        if block in self.block_data:
            self.block_data[block].append(str(index))
        else:
            self.block_data[block] = [str(index)]






    
