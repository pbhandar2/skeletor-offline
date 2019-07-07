# coding=utf-8
"""
The interface for trace readers.
Author: Pranav Bhandari <bhandaripranav94@gmail.com> 2018/11
"""

import abc


class AbstractReader(metaclass=abc.ABCMeta):
    __metaclass__ = abc.ABCMeta

    def __init__(self, file_loc):
        """
        Initializing abstract trace reader.
        :param file_loc: location of the file
        """

        self.file_loc = file_loc

    @abc.abstractclassmethod
    def get_next_line(self):
        """
        read one request, only return the label of the request
        :return:
        """
        pass

    @abc.abstractclassmethod
    def skip_lines(self, num_lines):
        """
        read one request, only return the label of the request
        :return:
        """
        pass
