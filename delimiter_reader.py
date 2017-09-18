#!/usr/bin/env python

import argparse
import csv
import os
import sys
import time

class DelimiterReaderException(Exception):
    pass

class DelimiterReader(object):
    """DelimitedReader is a class for manipulating columnar data separated by
    various delimiters. Data can be sorted by a single column as well as
    accessed via web service.

    """
    def __init__(self):
        self.rows = []

    def row_birthdate_to_ts(self, row_tuple):
        converted = []
        # Populate the new list with the first four elements
        converted = row_tuple[:-1]
        # Split the last element into its constituent month, day, and year pieces
        month, day, year = row_tuple[-1].split('/')
        # Create a time_struct object using the date components
        tm = time.struct_time((int(year), int(month), int(day), 0, 0, 0, 0, 0, 0))
        # Convert the time_struct value to an epoch time
        ts = long(time.mktime(tm))
        # Append the epoch time to the new list
        converted.append(ts)
        return converted

    def row_ts_to_birthdate(self, row_tuple):
        converted = []
        # Populate the new list with the first four elements
        converted = row_tuple[:-1]
        # Convert the final element, the birthdate as an epoch time, to a time_struct
        tm = time.localtime(row_tuple[-1])
        # Represent the birthdate in MM/DD/YYYY format
        birthdate = time.strftime('%m/%d/%Y', tm)
        # Append the birthdate to the new list
        converted.append(birthdate)
        return converted

    def detect_dialect(self, input_file):
        """Given an input file, utilize the csv.Sniffer() class to determine
        the dialect of the file.  Any axceptions raised by this method must be
        caught by the caller.

        """

        with open(input_file, 'rb') as in_fd:
            input_file_dialect = csv.Sniffer().sniff(in_fd.read(2048))
        return input_file_dialect

    def read_file(self, input_file):
        """Given an input file, parses the input into a list of lists, storing
        the results in the class variable `rows'.

        Returns: None

        """

        try:
            # Attempt to determine the dialect of the input file
            input_file_dialect = self.detect_dialect(input_file)
            with open(input_file, 'rb') as in_fd:
                d_reader = csv.reader(in_fd, input_file_dialect)
                for row in d_reader:
                    row_with_ts = self.row_birthdate_to_ts(row)
                    self.rows.append(row_with_ts)
        except (IOError, OSError, csv.Error) as exc:
            raise DelimiterReaderException("Failed to parse file: {} "
                                  "({})".format(input_file, exc))
    def sort_gender_then_lastname(self):
        self.rows.sort(key=lambda x: (x[2], x[0]))

    def sort_birthdate(self):
        self.rows.sort(key=lambda x: x[4])

    def sort_lastname(self, descending=False):
        self.rows.sort(reverse=descending)

    def print_rows(self):
        for row in self.rows:
            row_with_birthdate = self.row_ts_to_birthdate(row)
            print "{} {} {} {} {}".format(row_with_birthdate[0],
                                          row_with_birthdate[1],
                                          row_with_birthdate[2],
                                          row_with_birthdate[3],
                                          row_with_birthdate[4])

