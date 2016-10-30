#!/usr/bin/python

import pycurl
import json
from StringIO import StringIO

BASEURL='http://data.neonscience.org/api/v0/'

buff = StringIO()
c = pycurl.Curl()
c.setopt(c.URL, BASEURL+'sites')
c.setopt(c.WRITEDATA, buff)
c.perform()
c.close()

body = buff.getvalue()
neonSites = json.loads(body)

for site in neonSites['data']:
  print site['siteCode'], 
  print site['siteName'], 
  print site ['siteType']
  for product in site['dataProducts']:
    print "  "+product['dataProductCode'],
    print "  "+product['dataProductTitle']

