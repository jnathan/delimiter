#!/usr/bin/env python

import sys
from flask import Flask

import delimiter_reader

app = Flask(__name__)
dr = delimiter_reader.DelimiterReader()

@app.route('/records/gender', methods=['GET'])
def get_records_by_gender():
    dr.sort_gender()
    return dr.render_rows(fmt='json')

@app.route('/records/birthdate', methods=['GET'])
def get_records_by_birthdate():
    dr.sort_birthdate()
    return dr.render_rows(fmt='json')

@app.route('/records/name', methods=['GET'])
def get_records_by_lastname():
    dr.sort_lastname()
    return dr.render_rows(fmt='json')

if __name__ == '__main__':
    app.config['data_files'] = sys.argv[1:]
    if len(app.config['data_files']) < 1:
        sys.stderr.write("usage: {} [input-file [input-file "
                         "...]]\n".format(sys.argv[0]))
        sys.exit(1)
    else:
        for _datafile in app.config.get('data_files'):
            print "reading {}".format(_datafile)
            dr.read_file(_datafile)
    app.run(debug=True)
