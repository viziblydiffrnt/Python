import os
import sys, getopt
import requests
import json
import re
import time
import datetime
import calendar

class restApiClient(object):

    def __init__(self,taskParams):
        '''
        required:
            authToken: Token required for querying API
            base_path: Location to write file output
            fileName: Name of the output file (including file extension)
            url: URL for API query
            method: API call method (GET, POST, PUT, etc.)
        optional:
            query: Query for API
            queryRequired (derived): If a value is present for query, set to True, else False

        '''
        try:

            self.authToken = taskParams["auth"]
            self.base_path = taskParams["outputPath"]
            self.fileName = taskParams["outputFile"]
            self.url = taskParams["url"]
            self.query = taskParams["query"]
            self.queryRequired = taskParams["queryRequired"]
            self.method = taskParams["method"]
            self.flattenJson = taskParams["flatten"]

            print "auth={}".format(self.authToken)
            print "basepath={}".format(self.base_path)
            print "fileName={}".format(self.fileName)
            print "queryRequired={}".format(self.queryRequired)
            print "query={}".format(self.query)
            print "url={}".format(self.url)
            print "method={}".format(self.method)
            print "flatten={}".format(self.flattenJson)

        except Exception as err:
            print "Unexpected Error while initializing the class with ERROR: {}".format(err)
            sys.exit(1)


    def apiRequest(self,outputType='JSON'):
        '''
        Returns the response from the API query formatted based on the outputType value.
        Default is JSON, CSV is also supported.
        '''
        try:
            if outputType == 'JSON':
                ct = "application/json"
            elif outputType == 'CSV':
                ct = "text/csv"
            headers = {"x-auth-token":self.authToken, "content-type":ct}
            method = self.method
            finalUrl = self.url

            if self.queryRequired == True:
                payload = self.query
                responseJson = requests.request(method, finalUrl, headers=headers, data=payload)
            else:
                responseJson = requests.request(method, finalUrl, headers=headers, verify=False)

            if responseJson.status_code != 200:
                print "Unexpected Error while querying the API with ERROR: {}".format(responseJson.text)
                sys.exit(1)
            else:
                if outputType == 'JSON':
                    apiResponse = responseJson.json()
                elif outputType == 'CSV':
                    apiResponse = (responseJson.text).encode('UTF8')
                return apiResponse

        except Exception as err:
            print "Unexpected Error while querying the API with ERROR: {}".format(err)
            sys.exit(1)


    def outputJsonToFile(self, jsonParam):
        '''
        Input JSON, write to file path specified in argv
        '''
        flatten = self.flattenJson

        # Create directory for output
        try:
            fileDir = self.base_path
            if not os.path.exists(fileDir):
                os.makedirs(fileDir)
        except Exception as err:
            print "Error Creating the output Dir ERROR: {}".format(err)
            sys.exit(1)

        output_file = self.base_path+self.fileName

        if flatten == "True":
            jsonOut = "\n".join([json.dumps(i) for i in jsonParam])
        else:
            jsonOut = jsonParam


        try:
            with open(output_file,'w') as f:
                f.write(jsonOut)
        except Exception as err:
            print "Error Writing the output File ERROR: {}".format(err)
            sys.exit(1)


def getParams(argv):

    auth = None
    outputPath = None
    outputFile = None
    url = None
    query = None
    method = None
    flatten = None

    params = {}

    opts, args = getopt.getopt(argv,"a:p:f:u:q:m:j:", ["auth=","path=","file=","url=","query=","method=","flattenJson="])
    for opt,arg in opts:
        if opt in ("-a","--auth"):
            auth = arg
            params["auth"] = auth
        elif opt in ("-p","--path"):
            outputPath = arg
            params["outputPath"] = outputPath
        elif opt in ("-f","--file"):
            outputFile = arg
            params["outputFile"] = outputFile
        elif opt in ("-u","--url"):
            url = arg
            params["url"] = url
        elif opt in ("-q","--query"):
            query = arg
            params["query"] = query
        elif opt in ("-m","--method"):
            method = arg.upper()
            params["method"] = method
        elif opt in ("-j","--flattenJson"):
            flatten = arg
            params["flatten"] = flatten

    for f in ['url','method','outputPath','outputFile']:
        if f not in params.keys():
            # Force hard error
            print "ERROR: %s not provided." % (f)
            sys.exit(1)

    if not query:
        params["query"] = None
        params["queryRequired"] = False
    else:
        params["queryRequired"] = True

    return params

    # Initialize
    # client = restApiClient(params)
    #
    # # Get data from API
    # clientOutput = client.apiRequest()
    #
    # # Write output to file
    # client.outputJsonToFile(clientOutput)


if __name__=='__main__':
    params = getParams(sys.argv[1:])

    # Initialize
    client = restApiClient(params)

    # Get data from API
    clientOutput = client.apiRequest()

    # Write output to file
    client.outputJsonToFile(clientOutput)
