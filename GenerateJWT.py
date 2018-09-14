#!/usr/local/bin/python3
import sys, getopt
import http.client
import urllib
import re
import base64
import jwt


'''
	Python Function created to generate a JWT Token.
	This function built in order to be possible to call it from a shell script, with parameters.
	
	call example:
	/usr/bin/python3 /home/pedrolourenco/Desktop/pythonTestFunctionV2.py --tenantID something --secretKey somethingElse 
	
	This was done for a specific set of parameters, but its basis should work as a example to other developments.
'''

def main(argv):
   tenantId = ''
   secretKey = ''
   try:
      opts, args = getopt.getopt(argv,"ht:s:",["tenantId=","secretKey="])
   except getopt.GetoptError:
      print ('generatejwt.py -t <tenantId> -s <secretKey>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print ('generatejwt.py -t <tenantId> -s <secretKey>')
         sys.exit()
      elif opt in ("-t", "--tenantId"):
         tenantId = arg
      elif opt in ("-s", "--secretKey"):
         secretKey = arg
		 
   secretKey=bytes(secretKey,encoding='ascii')
  
   #encode the encoded secret
   encodedSecret = base64.b64encode(secretKey)
   #Generate the JWT
   token = jwt.encode({'clientID': tenantId}, encodedSecret, algorithm='HS256')
   print (bytes.decode(token))  
   

if __name__ == "__main__":
   main(sys.argv[1:])