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
        """Given a row (a list of five elements) in the form:
        last name, first name, gender, favorite color, and birthdate,
        convert the MM/DD/YYYY birthdate into an epoch time so it can be
        sorted.

        Returns: a copy of the original row, with the former string birthdate
        converted to an an epoch timestamp.

        """
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
        """Given a row (a list of five elements) in the form:
        last name, first name, gender, favorite color, and birthdate,
        convert the epoch timestamp birthdate into an MM/DD/YYYY string so it can
        be printed.

        Returns: a copy of the original row, with the former epoch timestamp
        birthdate converted to an MM/DD/YYYY string.

        """
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

    def detect_dialect(self, in_fd):
        """Given an input file descriptor, utilize the csv.Sniffer() class to determine
        the dialect of the file.  Any axceptions raised by this method must be
        caught by the caller.

        """

        input_file_dialect = csv.Sniffer().sniff(in_fd.read(2048))
        in_fd.seek(0)
        return input_file_dialect

    def read_file(self, input_file):
        """Wrapper function for reading rows of data from files on disk. Calls
        read_rows() to actually read the rows of data.

        Returns: None

        """

        try:
            # Attempt to determine the dialect of the input file
            with open(input_file, 'rb') as in_fd:
                self.read_rows(in_fd)
        except (IOError, OSError, csv.Error) as exc:
            raise DelimiterReaderException("Failed to parse file: {} "
                                  "({})".format(input_file, exc))

    def read_rows(self, in_fd):
        """Given an input file descriptor, parses the input into a list of lists,
        storing the results in the class variable `rows'.

        Returns: None

        """
        input_file_dialect = self.detect_dialect(in_fd)
        d_reader = csv.reader(in_fd, input_file_dialect)
        line_number = 1
        for row in d_reader:
            try:
                # Check to ensure that each line has 5 fields
                if len(row) != 5:
                    raise ValueError("Incorrect number of fields")
                else:
                    row_with_ts = self.row_birthdate_to_ts(row)
                    self.rows.append(row_with_ts)
            except ValueError as exc:
                sys.stderr.write("Skipping invalid data at line number {:d}\n".format(line_number))
                sys.stderr.write("Erring line generated error: {}\n").format(exc)
                line_number += 1

    def sort_gender_then_lastname(self):
        """Sorts all rows in-place: first by gender, and then by last name."""
        self.rows.sort(key=lambda x: (x[2], x[0]))

    def sort_birthdate(self):
        """Sorts all rows in-place by birthdate."""
        self.rows.sort(key=lambda x: x[4])

    def sort_gender(self):
        """Sorts all rows in-place by gender."""
        self.rows.sort(key=lambda x: x[2])

    def sort_lastname(self, descending=False):
        """Sorts all rows in-place by lastname, defaults to a decending
        sort."""
        self.rows.sort(reverse=descending)

    def render_rows(self, fmt='str'):
        """Given a format either: 'str' or 'json', returns a list of all the
        rows as space delimited strings or a JSON document of all
        rows.

        """

        _rows = map(self.row_ts_to_birthdate, self.rows)
        if fmt == 'str':
            _rows = ["{} {} {} {} {}".format(r[0], r[1], r[2], r[3], r[4]) for r in _rows]
            return _rows
        elif fmt == 'json':
            return(json.dumps(_rows))
