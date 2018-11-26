# coding=utf-8

"""
The I/O profiler that gives the users the I/O metrics.
Author: Pranav Bhandari <bhandaripranav94@gmail.com> 2018/11
"""

from traceReader.abstractReader import AbstractReader

# it wouldn't work without this in mjolnir
import matplotlib
matplotlib.use("agg")

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
        self.data = {
            "time": [],
            "access_time": []
        }
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
        start = self.data["access_time"][0]
        bucket_array = [start]
        for t in self.data["access_time"][1:]:
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
        """
        Get the access pattern in matrix form. Each row correspond to an LBNs access pattern 
        over time. 
        Params:
            filename -- the filename to use to save the matrix data
        """

        if (self.length == -1):
            metric_calculator()

        f = open(filename, "w+")

        blocks = sorted(list(self.block_list), reverse=True)
        for block in blocks:
            f.write(self.generate_matrix_row(block))
            f.write('\n')

        # keys =  self.block_data.keys()

        # for key in sorted(keys, reverse=True):
        #     print(key)
        #     v = self.block_data[key]
        #     f.write(" ".join(map(str, self.get_access_matrix_row(v))))
        #     f.write("\n")


    def generate_matrix_row(self, block):
        block_data = self.block_data[block]
        # print("We are in generate_matrix_row for block {}".format(block))
        # print(self.block_data)
        data_found = 0;
        v = self.block_data[block]
        data_string = ''
        first_entry = v[0]
        if (first_entry in block_data):
            data_string="{}".format(1)
        else:
            data_string="{}".format(0)
        

        for i in range(1, self.reader.num_lines):
            if (i in v):
                data_string += ",{}".format(1)
            else:
                data_string += ",{}".format(0)

        return data_string

        # for block in blocks[:1]:
        #     v = self.block_data[key]
        #     print(",".join(map(str, self.get_access_matrix_row(v))))

        # first_entry = block_data[0]
        # if (first_entry in block_data) {
        #     data_string="{}".format(1)
        # } else {
        #     data_string="{}".format(0)
        # }

        # for i in range(1, self.reader.num_lines):
        #     if (i in block_data):
        #         #print("The block was accessed at {}".format(i))
        #         data_string = data_string + "," + str(1)
        #         data_found += 1
        #     else:
        #         data_string = data_string + "," + str(0)

        # print("Data found for the block {} and the total block data {}".format(data_found, len(block_data)))
        # print(data_s)


    def get_access_matrix_row(self, index):
        """
        Based on at which indexes that the block is accessed, create the matrix rows. 
        Params:
            index -- array of indexes where a block was accessed. 
        """
        row = [0] * len(self.data["access_time"])
        for i in index:
            row[i] += 1
        return row

    def update_data(self, line_data):
        """
        Once the data is extracted from a line. This function is used to update the data for 
        each data extracted from the line. 
        Params:
            line -- The data extracted from a line. 
        """
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
        """
        Uses the field dict to extract all the information that it can from a given 
        line. 
        Params:
            line -- the line in string form. 
        """
        line_data = {}
        for field in self.reader.fields:
            field_object = self.reader.fields[field]
            field_type = field_object["type"]
            field_index = field_object["index"]
            line_array = line.split(self.reader.delimiter)
            line_data[field] = func_map[field_type](line_array[field_index])

        return line_data

    def update_field(self, field, field_value, update_type):
        """
        This functions updates a given field of the data dictionary.  
        Params:
            field -- the field to be updated.
            field_value -- tthe value of the field
            update_type -- what kind of update to perform, append, add, subtract? 
        """
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

    def plot_scatter_interval(self, field, file_name, interval, colorField=None, markerSize=1, binSize=0):
        '''
            Need to find the index to start and end reading the data for a given time interval 
            Then just call plot scatter with the start and end index and plot just for that 
        '''

        if (self.length == -1):
            self.metric_calculator()

        time_length = self.reader.clock.time_elapsed()
        num_bins = math.floor(time_length/interval)

        for i in range(num_bins):

            start_index, end_index = self.get_interval_index([i*interval, (i+1)*interval])

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
                time = self.data["access_time"]

            print("The len of time is {}".format(len(time)))
            print("The len of the data is {}".format(len(self.data[field])))

            plt.figure(i)
            plt.scatter(time[start_index:end_index], self.data[field][start_index:end_index], color=color_array, s=markerSize, alpha=0.1)
            plt.xlabel("time")
            plt.ylabel(field)
            plt.ylim(0, max(self.data[field]))
            plt.title("time vs {}".format(field))
            plt.savefig("{}_{}".format(str(start_index), file_name), dpi=1200)
            plt.close()

        #plot_scatter(self, field, file_name, colorField, markerSize, binSize)

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
            time = self.data["access_time"]

        print("The len of time is {}".format(len(time)))
        print("The len of the data is {}".format(len(self.data[field])))

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
        Do proessing based on the value of the size in line data. If the access is of size 1024
        and the block size is 512 then it means that the current and the next block is accessed 
        and both need to be accounted for. 
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
            self.process_block(int(cur_block), len(self.data["access_time"]))
            cur_block += block_size

        #print("Processing size completed.")


    def process_block(self, block, index):
        """
        Update information on the blocks. A set maintains the unique blocks and blocks_data maintains
        the access pattern of each block. 
        Params:
            block -- the block number. 
            index -- this represents the current time 
        """
        # print("Processing the block {}".format(block))
        self.block_list.add(block)
        if block in self.block_data:
            self.block_data[block].append(index)
        else:
            self.block_data[block] = [index]


    def get_interval_index(self, interval):
        time = self.data["access_time"]
        start_time = time[0]
        start_index = -1
        end_index = -1
        cur_index = 0
        start = interval[0]
        end = interval[1]

        for t in time:
            diff = (t - start_time)/1000000000 # time in nanosecond 
            if (diff >= start and start_index == -1):
                start_index = cur_index
            elif (diff > end and end_index == -1):
                end_index = cur_index - 1
                break
            cur_index += 1

        return start_index, end_index








    
