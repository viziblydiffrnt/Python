import os, sys
from os import path
import more_itertools
from  more_itertools import unique_everseen
from operator import itemgetter
from pprint import pprint
import json
import xml.etree.ElementTree as ET
import xmltodict
import csv

# Load json into dictionary
json_object = json.load(open('/Users/mark.jacobson/Desktop/sample json.json'))

# Pretty print json
pprint(json_object)

# Loop through json structure
for k,v in json_object.iteritems():
    print "the key is %s" % (k)
    print "and its value is %s" % (v)
    for i,j in v.iteritems():
        print "the next key is %s" % (i)
        print "and its value is %s" % (j)
        # pprint(i)

# Load xml
with open('/Users/mark.jacobson/Desktop/sample xml.xml') as fd:
    xml_object = xmltodict.parse(fd.read())

print xml_object['widget']
print xml_object['widget']['debug']
print xml_object['widget']['window']

# Load data from csv
with open('/Users/mark.jacobson/Desktop/foo.csv','rb') as f:
    reader = csv.reader(f)
    for row in reader:
        print row
