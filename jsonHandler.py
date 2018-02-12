#!/usr/bin/env python

import sys
import json

def flattenJson(init, lkey=''):
    ret = {}
    for rkey, val in init.items():
        key = lkey+rkey
        if isinstance(val,dict):
            # print '%s is a dict' % (rkey)
            ret.update(flattenJson(val,key+'_'))

        # elif isinstance(val,list):
        #     l = []
        #     for v in val:
        #         if isinstance(v,dict):
        #             l.append(flattenJson(v,key+'_'))
        #             # ret.update(l)
        #         else:
        #             l.append(v)
        #     ret[key] = l

        else:
            # print '%s is a value' % (rkey)
            ret[key] = val
    return ret




# line = open('/home/mark_jacobson/local_pipeline/KH-Analytics/test/py/source_catalog/source_catalog_20170501.json','r')
# json_data = line.read().split("\t")
# for i in json_data:
#     jsonRecord = json.loads(i)
# for i in jsonRecord[:1]:
#     print json.dumps(flattenJson(i))
