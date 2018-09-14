#!/usr/local/bin/python3
import requests
import json
import urllib
import time
from requests.auth import HTTPBasicAuth 
import sys, getopt
import httplib
import urllib
import re
import base64
import jwt
import codecs


'''
	Python Function created to read data from a REST API, usic basic auth.
	This function built in order to be possible to call it from a shell script, with parameters.
	
	call example:
	/usr/bin/python3 /home/pedrolourenco/Desktop/pythonTestFunctionV2.py --username user@mail.com --password DemoPassword --descriptorID 81b5d233-9043-407b-ab63-b4b6ccf666db --descriptorName all_engage_data --exportStartTime 2018-05-10T09:00:00Z --exportEndTime 2018-07-02T23:59:59Z --outputFilename /home/pc_user/Documents/data.csv	
	
	This was done for a specific API, but its basis should work as a example to other developments.
'''

def main(argv):
    username = ''
    password = ''
    descriptorID = ''
    descriptorName = ''
    exportStartTime = ''
    exportEndTime = ''
    outputFilename = ''

    try:
        opts, args = getopt.getopt(argv, "ha:b:c:d:e:f:g:", [
                                   "username=", "password=", "descriptorID=", "descriptorName=", "exportStartTime=", "exportEndTime=", "outputFilename="])
    except getopt.GetoptError:
        print('generatejwt.py -t <username> -s <password>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('generatejwt.py -t <username> -s <password> ')
            sys.exit()
        elif opt in ("-a", "--username"):
            username = arg
        elif opt in ("-b", "--password"):
            password = arg
        elif opt in ("-c", "--descriptorID"):
            descriptorID = arg
        elif opt in ("-d", "--descriptorName"):
            descriptorName = arg
        elif opt in ("-e", "--exportStartTime"):
            exportStartTime = arg
        elif opt in ("-f", "--exportEndTime"):
            exportEndTime = arg
        elif opt in ("-f", "--outputFilename"):
            outputFilename = arg
    
    print()
    print("Username: "+username)
    print("Password: " + password)
    print("Descriptor ID: " + descriptorID)
    print("Descriptor Name: " + descriptorName)
    print("Export Start Time: " + exportStartTime)
    print("Export End Time: " + exportEndTime)
    print("Output Filename: " + outputFilename)

    payload = {
        "exportDescriptors": [
            descriptorID  # ADD YOUR DESCRIPTOR ID
        ],
        "contentName": descriptorName,  # ADD THE NAME OF THE DESCRIPTOR
        "interval": 0,
        "startTime": exportStartTime,  # SELECT THE DATA STARTING DATE
        "endTime": exportEndTime,  # SELECT THE DATA ENDING DATE
        "exportNow": "true"
    }
	
    http_proxy  = "<proxyHost:proxyPort>"
    https_proxy = "<proxyHost:proxyPort>"

    proxyDict = { 
              "http"  : http_proxy, 
              "https" : https_proxy
            }

    payload = json.dumps(payload)

    headers = {'content-type': 'application/json'}


    print(headers)
    # Add the user and password for this part
    print('\n\n\n\n')
    print('---------------------Submitting Export Request to CI360--------------------------')
    r = requests.post('<API_URL>',
                    auth=HTTPBasicAuth(username, password), data=payload, headers=headers, proxies=proxyDict)
    print (r.content)
    print(r.status_code, r.reason)
    # print(r.text)

    # We are creating a variable with the json content and only taking the text of the ID

    descriptorexportado = json.loads(r.text)

    iddeldescriptor = descriptorexportado['id']

    # print(iddeldescriptor) #Not necessary to do, just to check our variable has the ID correctly

    # Here we are downloading the URLS from were the data is going to be downloaded

    # Add the user and password for this part

    # Wait 1 minute unetil our call is ready because the process takes a little bit

    r = requests.get('<API_URL>' %
                    iddeldescriptor, auth=HTTPBasicAuth(username, password), proxies=proxyDict)
    print(r.content)
    print(r.status_code, r.reason)

    obj = json.loads(r.content)

    print('-------------EXPORT_REQUEST_INFO------------------')
    print('\n\n')


    links = obj['links']
    status = obj['status']

    getPortion = links[0]
    getHref = getPortion['href']


    print('Checking Export Status...\n')

    while(status != 'EXPORTED'):
        print('Export Request not ready, status: ' + status + '. please wait...\n')
        time.sleep(15)
        r = requests.get(getHref, auth=HTTPBasicAuth(username,password), proxies=proxyDict)
        obj = json.loads(r.content)
        status = obj['status']


    print('Export Request has been processed, commencing data download!\n')

    downloadItems = obj['downloadItems']


    # The name of the file can be personalized
    print('-----------DATA_DOWNLOAD-------------')
    myfile = codecs.open(outputFilename, 'w', 'utf-8')
    for i in list(reversed(downloadItems)):
        print(i['url'])
        r = requests.get(i['url'], proxies=proxyDict)
        print(r.status_code, r.reason)
        myfile.write(r.text)
        
    myfile.close()
    print('-----------DOWNLOAD_COMPLETED-------------\n')


if __name__ == "__main__":
    main(sys.argv[1:])
