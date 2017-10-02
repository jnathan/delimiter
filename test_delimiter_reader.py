#!/usr/bin/env python

import sys

import nose
from nose.tools import *

import delimiter_reader

@raises(ValueError)
def test_row_birthdate_to_ts_1():
    dr = delimiter_reader.DelimiterReader()
    row = ['Simpson', 'Homer', 'Male', 'Orange', '123']
    dr.row_birthdate_to_ts(row)

def test_row_birthdate_to_ts_2():
    dr = delimiter_reader.DelimiterReader()
    row = ['Simpson', 'Homer', 'Male', 'Orange', '5/12/1956']
    row_birthdate_ts = dr.row_birthdate_to_ts(row)
    assert_equal(row_birthdate_ts, ['Simpson', 'Homer', 'Male', 'Orange', -430423200L])

@raises(delimiter_reader.DelimiterReaderException)
def test_read_file1():
    dr = delimiter_reader.DelimiterReader()
    dr.read_file('asasdfa')

def test_read_file2():
    sys.path.append('test')
    import test_read_file2_rows
    dr = delimiter_reader.DelimiterReader()
    dr.read_file('test/test_read_file2_space.dat')
    assert_equal(dr.rows, test_read_file2_rows.rows)
    sys.path.pop()
