#!/usr/bin/env python

import argparse
import os
import sys

import delimiter_reader

def main(args):
    dp = delimiter_reader.DelimiterReader()
    for input_file in args.files:
        dp.read_file(input_file)
    if args.mode == 'Output1':
        dp.sort_gender_then_lastname()
    elif args.mode == 'Output2':
        dp.sort_birthdate()
    elif args.mode == 'Output3':
        dp.sort_lastname(descending=True)
    dp.print_rows()
    #print "\n\nAfter sorting by birthdate\n\n"
    #dp.sort_gender()
    #dp.print_rows()

if __name__ == '__main__':
    epilog = ("\n\nmode is one of:\n\n"
             "Output1: sorted by gender, then by last name, ascending\n"
             "Output2: sorted by birthdate, ascending\n"
             "Output3: sorted by last name, descending\n")

    ap = argparse.ArgumentParser(description='Delimiter file utility',
                                 formatter_class=argparse.RawDescriptionHelpFormatter,
                                 epilog=epilog)
    ap.add_argument('files', nargs='*', help='Input files to be processed')
    ap.add_argument('-mode', type=str, default='Output1',
                    help='Specifies the output mode. One of: Output1, Output2, or Output3')
    args = ap.parse_args()
    #print dir(ap)
    if args.mode not in ['Output1', 'Output2', 'Output3']:
        sys.stderr.write("\nError: Invalid output mode argument")
        sys.stderr.write(ap.epilog)
        sys.exit(1)
    main(args)
