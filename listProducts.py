#!/usr/bin/python

import pycurl
import json
from StringIO import StringIO

BASEURL='http://data.neonscience.org/api/v0/'

buff = StringIO()
c = pycurl.Curl()
c.setopt(c.URL, BASEURL+'products')
c.setopt(c.WRITEDATA, buff)
c.perform()
c.close()

body = buff.getvalue()
neonProducts = json.loads(body)

for product in neonProducts['data']:
  print product['productCode'], 
  print product['productStatus'], 
  print product ['productDescription']


