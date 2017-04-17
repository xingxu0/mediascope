import sys
import urllib2, urllib, pickle

port_f = open('../config/port.info')
ports = port_f.read().split('|')
PORT = ports[0]


URL='http://128.125.121.204:' + PORT
d = [(sys.argv[1], sys.argv[2])]
req = urllib2.Request(URL, urllib.urlencode(d))
u = urllib2.urlopen(req)


