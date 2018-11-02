# coding=utf-8

"""
The I/O profiler that gives the users the I/O metrics.

Author: Pranav Bhandari <bhandaripranav94@gmail.com> 2018/11
"""

from traceReader.abstractReader import AbstractReader
import matplotlib.pyplot as plt

func_map = {
    "float":  lambda x: float(x),
    "integer": lambda x: int(x),
    "string": lambda x: str(x)
}

class IOProfiler():

    def __init__(self, reader):

        assert isinstance(reader, AbstractReader), \
            "This is not a valid reader: {}".format(reader)

        self.reader = reader
        self.data = {}
        self.min_max_data = {}
        self.offset = {}
        self.length = -1

    def get_time_length(self):
        """
        Returns the length of the trace file.
        """
        if (self.length == -1):
            metric_calculator()
        return self.length

    def bucket_time(self, bucket_size):
        """
        Returns the time array with buckets
        """
        bucket_array = []
        start = -1
        for t in data["time"]:
            if (start >= 0):
                diff = t - start
                if (diff > 1000000000 * bucket_size):
                    bucket_array.append(t)
                    start = t
            else:
                start = t
                bucket_array.append(t)

        return bucket_array

    def get_access_data(self):
        print("This function should return the data needed to create the plot that we need. The data would have to be LBN vs Time but \
        would I also encode the read/write situation? What we would need is an array with [[array of time] [array of lbn] [array of R/W]]")

    def metric_calculator(self):
        """
        Calculates the metric of the file.
        """
        # going through each line
        line = self.reader.get_next_line()
        start_time = -1
        while(line):

            # the fields provided by the user
            for field in self.reader.fields:
                field_object = self.reader.fields[field]
                field_type = field_object["type"]
                field_index = field_object["index"]
                line_array = line.split(self.reader.delimiter)

                if (field == "io_type"):
                    field_value = self.process_io_type(line_array, field_index, field_object["values"])
                elif (field == "time"):
                    cur_time = func_map[field_type](line_array[field_index])
                    field_value = cur_time
                    # record the start time
                    if (start_time == -1):
                        start_time = cur_time
                elif (field == "size"):
                    field_value = func_map[field_type](line_array[field_index])
                else:
                    field_value = func_map[field_type](line_array[field_index])

                # if the field is in the data struct
                if field in self.data:
                    self.data[field].append(field_value)
                    min_max_array = self.min_max_data[field]
                    if (field_type == "integer" or field_type == "float"):
                        self.min_max_data[field] = [min(field_value, min_max_array[0]), max(field_value, min_max_array[1])]
                else:
                    self.data[field] = [field_value]
                    self.min_max_data[field] = [field_value, field_value]

            line = self.reader.get_next_line()

        self.length = cur_time - start_time
        print(self.min_max_data)

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




    def plot_distribution(self, field, file_name, colorField=None):
        """
        Plots the distribution of the given field over time.
        """
        print("Plot distribution of {}".format(field))
        plt.plot(self.data["time"], self.data[field])
        plt.xlabel("time")
        plt.ylabel(field)
        plt.title("time vs {}".format(field))
        plt.savefig(file_name, dpi=1200)

    def plot_scatter(self, field, file_name, colorField=None, markerSize=1):
        """
        Saves a scatterplot of the given field.
        Params:
            field -- the field that is going to be plotted
            file_name -- the output file name
            colorField -- the field that will dictate the color of the points
            markerSize -- the size of the marker
        """
        print("Scatter plot of {}".format(field))

        colors = ["red", "gold", "darkgreen", "navy", "black"]

        color_map = {
            "read": "r",
            "write": "b"
        }
        color_array = [color_map[x] for x in self.data["io_type"]]

        plt.scatter(self.data["time"], self.data[field], color=color_array, s=markerSize, alpha=0.1)
        plt.xlabel("time")
        plt.ylabel(field)
        plt.ylim(0, max(self.data[field]))
        plt.title("time vs {}".format(field))
        plt.savefig(file_name, dpi=1200)

    def process_io_type(self, line_array, index, values):
        """
        Processes the i/o type for each line.
        Params:
            line_array -- the line broken down using the delimiter
            index -- the index of the io_type field
            values -- the values that the i_o type field takes
        """
        rw_value = line_array[index]
        for val in values:
            if(values[val] == rw_value):
                return val
        raise Exception("The value {} is not a included in the fields object.".format(rw_value))
