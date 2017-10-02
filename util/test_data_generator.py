
import sys

import nose
from nose.tools import *

import data_generator

@raises(ValueError)
def test_generate_birthday1():
    data_generator.generate_birthday(-1, 11)

@raises(ValueError)
def test_generate_birthday2():
    data_generator.generate_birthday(3, 14)
