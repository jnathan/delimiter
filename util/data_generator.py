#!/usr/bin/env python

"""Generates three delimited input test files: a pipe delimited file, a comma
delimited file, and a space delimited file. Each row is composed of rows with
each row composed of five fields:
last name, first name, gender, favorite color, and birthdate.

"""

import argparse
import csv
import os
import random
import sys
import time

# Relative from the current working directory, directory name of the census files
DATA_DIR = 'census_files'


def generate_birthday(year, month):
    """Given a year and month, return a day that falls within the month,
    accounting for leap years.

    Returns a string in the form: MM/DD/YYYY
    Returns an epoch time as an integer

    """

    leap_year = False


    # April, June, and November have 30 days per-month
    if month in [4, 6, 11]:
        day = random.randint(1, 30)
    # February may have 29 days if the year is a leap year
    if month == 2:
        # If the year is evenly divisible by 4
        if year % 4 == 0:
            # And if the year is evenly divisble by 100 and 400 it's a leap year
            if year % 100 == 0:
                if year % 400 == 0:
                    leap_year = True
                # A year evenly divisible by 4, and divisible by 100 but not
                # 400 is not a leap year
                else:
                    leap_year = False
            # A year evenly divisible by 4, but not 100 is also a leap year
            else:
                leap_year = True
        if leap_year is True:
            day = random.randint(1, 29)
        else:
            day = random.randint(1, 28)
    # January, March, May, July, August, September, October, and December have
    # 31 days
    else:
        day = random.randint(1, 31)

    # Create a struct_time object using the data from above
    #tm = time.struct_time((year, month, day, 0, 0, 0, 0, 0, 0))

    # Convert the struct_time object to an epoch time
    #ts = int(time.mktime(tm))
    # Return it as a string
    #return str(ts)
    # Return the birthday as a string in the form MM/DD/YY
    return "{:d}/{:d}/{:d}".format(month, day, year)

def load_census_file(census_file):
    """Given a census file (a space delimited file where the first column is a
    name), load all non-comment lines from the file and return a list of
    results with the first letter in each element capitalized.

    """

    try:
        with open(os.path.join(DATA_DIR, census_file), 'r') as in_fd:
            # Read all the lines from the census data
            buf = in_fd.readlines()
            # Build a list of only the first column, with the first letter capitalized
            census_names = [x.split()[0].capitalize() for x in buf]
            return census_names
    except IOError as exc:
        sys.stderr.write("Unable to load census file: {} "
                         "({})\n".format(census_file, exc))
def main(rows_per_file):
    genders = ['Male', 'Female']
    colors = ['Red', 'Orange', 'Yellow', 'Green', 'Blue', 'Purple', 'Pink',
              'Brown', 'Black', 'White', 'Gray']

    male_first_names = load_census_file('male_first_names.txt')
    female_first_names = load_census_file('female_first_names.txt')
    last_names = load_census_file('last_names.txt')

    for sample_file, sample_delimiter in [('sample_pipe.dat', '|'),
                                          ('sample_csv.dat', ','),
                                          ('sample_space.dat', ' ')]:
        try:
            with open(sample_file, 'wb') as out_fd:
                delimiter_writer = csv.writer(out_fd, delimiter=sample_delimiter,
                                          quoting=csv.QUOTE_MINIMAL)
                i = 0
                # Iterate the passed-in number of rows per-file
                while (i < rows_per_file):
                    # Generate a row
                    last_name = random.choice(last_names)
                    gender = random.choice(genders)
                    if gender == 'Male':
                        first_name = random.choice(male_first_names)
                    else:
                        first_name = random.choice(female_first_names)

                    favorite_color = random.choice(colors)

                    year = random.randint(1920, 2017)
                    month = random.randint(1, 12)
                    date_of_birth = generate_birthday(year, month)
                    # Write the row
                    delimiter_writer.writerow([last_name, first_name, gender,
                                               favorite_color, date_of_birth])
                    # And increment our accumulator
                    i += 1
        except (OSError, IOError, csv.Error) as exc:
            sys.stderr.write("Unable to create output file: {} "
                             "({})\n".format(sample_file, exc))


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='Delimiter file generator')
    ap.add_argument('rows', type=int, help='The number of rows per-file')
    args = ap.parse_args()
    if args.rows <= 0:
        ap.error("rows must be a positive integer")
    main(args.rows)
