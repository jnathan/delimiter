#!/usr/bin/env python

from flask import Flask
import glob

import delimiter_reader

dr = delimiter_reader.DelimiterReader()
for _datafile in glob.glob('sample_*.dat'):
    dr.read_file(_datafile)

app = Flask(__name__)

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
    app.run(debug=True)
