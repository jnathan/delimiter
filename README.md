## Synopsis

A collection of tools for working with delimited (pipe, space, comma) data composed of 'rows' of five fields:
last name, first name, gender, favorite color, birthdate

Tools include:
util/data_generator.py: generates sample data files using 1990 US Census data
delimiter_util.py:      for working with data (sorting and printing)
delimiter_rest_api.py:  A REST API for simple data retrieval and creating new entries

## Installation

This tool chain requres Flask 0.12 and nose (for unit testing)

## REST API Reference

Four URIs are exposed via the REST interface:

GET  /records/gender    - returns records sorted by gender

GET  /records/birthdate - returns records sorted by birthdate (ascending)

GET  /records/name      - returns records sorted by last name (ascending)

POST /records           - posts a record composed of the fields, delimited using any of the delimiters listed
                          above. The post must use the parameter record in the form:
                          curl -X post "record=First|Last|Female|Orange|11/22/1963" http://localhost:5000/records

## Tests

To run unit tests simpy run the the run_tests.sh script

## License

GPL v3.0
