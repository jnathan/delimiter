#!/usr/bin/env python

import argparse
import csv
import json
import os
import sys
import time

class DelimiterReaderException(Exception):
    pass

class DelimiterReader(object):
    """DelimitedReader is a class for manipulating columnar data separated by
    the delimiters: ',' (comma or CSV), ' ' (space), and '|' (pipe).
    Data is in a row format, composed of five fields:
    last name, first name, gender, favorite color, and birthdate.

    Several accessor methods are available for sorting, reformatting
    birthdate from a string to an integer (for sorting), and marshalling data
    for either printing or for being returned in a JSON document.

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

    def sort_gender(self):
        self.rows.sort(key=lambda x: x[2])

    def sort_lastname(self, descending=False):
        self.rows.sort(reverse=descending)

    def render_rows(self, fmt='str'):
        _rows = map(self.row_ts_to_birthdate, self.rows)
        if fmt == 'str':
            _rows = ["{} {} {} {} {}".format(r[0], r[1], r[2], r[3], r[4]) for r in _rows]
            return _rows
        elif fmt == 'json':
            return(json.dumps(_rows))

