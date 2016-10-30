#!/usr/bin/python

import sys
import re
import json
from StringIO import StringIO
import pycurl

BASEURL='http://data.neonscience.org/api/v0/'

def readURLToBuffer( url, buff ):
  """Use pyCurl to read the contents of a 
  URL into a StringIO buffer.
  """
  if isinstance(buff, StringIO)==False:
    raise TypeError( "buff should be a StringIO instance")
    
  c = pycurl.Curl()
  c.setopt(c.URL, url)
  c.setopt(c.WRITEDATA, buff)
  c.perform()
  c.close()


def downloadNEONData( productCode, siteCode, yearMonth ):
  """Download data from the NEON API. 
  Puts the CSV files in the working directory with the same
  name as they have on the API. Also keeps the meta data in 
  JSON format.
  
  Arguments:
   
  productCode   [string] the product code, e.g.'DP1.00024.001'
  siteCode      [string] the site code, e.g. 'JORN'
  yearMonth     [string] date in 'yyyy-mm' format
  
  """
  
  URL=BASEURL+'data/'+productCode+'/'+siteCode+'/'+yearMonth+'?package=basic'
  buff = StringIO()
  readURLToBuffer(URL, buff)
  body = buff.getvalue()
  neonData = json.loads(body)

  for neonFile in neonData['data']['files']:

    #select only 30 minute data in this 
    #example and use curl to download
    fields=neonFile['name'].split('.')
    if fields[-3]=='030':

      readURLToBuffer(neonFile['url'], buff)
      parData = buff.getvalue()
 
      #seperate the json header 
      #from the csv formatted data
      decoder = json.JSONDecoder()
      jsonData, idx = decoder.raw_decode(parData)
      parData = parData[idx:].lstrip()

      #write the csv file
      with open(neonFile['name'], 'w') as outFile:
        outFile.write(parData)
 
      #write the header information
      #in this example in json format
      with open(neonFile['name']+'.meta', 'w') as outFile:
        json.dump(jsonData, outFile)


if __name__=="__main__":

  #set product, site and date
  #could add command line parser here
  productCode='DP1.00024.001'
  siteCode='JORN'
  yearMonth='2016-06'

  downloadNEONData( productCode, siteCode, yearMonth )

