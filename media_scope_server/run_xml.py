import time, os, copy, sys, random,threading
import BaseHTTPServer, urlparse, cgi,urllib, urllib2

ACCEPTOR_IP = 'http://128.125.121.204:7778'
xml_file = sys.argv[1]
def run_xml():
	f = open(xml_file,'r')
	http_client([('temp.xml', f.read())])
	f.close()
	
def http_client(d):
	req = urllib2.Request(ACCEPTOR_IP, urllib.urlencode(d))
	u = urllib2.urlopen(req)

if __name__ == '__main__':
	run_xml()
