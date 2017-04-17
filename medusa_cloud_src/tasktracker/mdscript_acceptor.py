import time, os, copy, sys, random, threading, socket, select
import BaseHTTPServer, urlparse, cgi
from xml.etree import ElementTree as ET

HOST_NAME = '128.125.121.204'
#HOST_NAME = '204.57.0.100'
#server

SIZE = 128
dict = {}
CONN = {}
name_to_pid = {}
soc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		
port_f = open('../config/port.info')
ports = port_f.read().split('|')
PORT_NUMBER = int(ports[0])
SOC_PORT = int(ports[1])

class ThreadClass(threading.Thread):
	def run(self):
		global CONN, name_to_pid
		soc.bind(('127.0.0.1',SOC_PORT))
		soc.listen(5)
		while True:
			soc_input = [soc]
			for (k, v) in CONN.iteritems():
				soc_input.append(v)
			print soc_input
			print str(name_to_pid)
			_in, _out, _exc = select.select(soc_input, [], [])
			for s in _in:
				if s == soc:
					(c,a) = soc.accept()
					print "accepted"
					pid = mrecv(c)
					pids = pid.split(' ')
					name_to_pid[pids[1]] = pids[0]
					print "id to pid: " + str(name_to_pid)
					print "vess pid: "+ pids[0]
					CONN[str(pids[0])] = c
		#			print "*****conn "+CONN
				else:
					temp = s.recv(1024)
					if len(temp) == 0:
						s.close()
					for (k, v) in CONN.iteritems():
						if s == v:
							print str(k) + ' connection closed.'
							del CONN[k]
							for (x, y) in name_to_pid.iteritems():
								if y == k:
									print "deleting " + str(x) + " " + str(y)
									del name_to_pid[x]
									break
							break
					
def msend(conn,msg):
	conn.send(msg + '\n')

def mrecv(conn):
	global SIZE
	data = ''
	while data.find('\n') == -1:
		data += conn.recv(SIZE)
	return data[:-1]

def run_medusascript(filenames):
	print filenames
	global CONN, soc
	for i in filenames:
		newpid = os.fork()
		if newpid == 0:
			cmd = "python mdserv2.py %s %s" % (i[0], i[1])
			print cmd
			os.system(cmd)
			os._exit(1)
		else:
			pids = (os.getpid(), newpid)
			print "parent: %d, child: %d" % pids

def change_id(before):
	global name_to_pid
	a = before.find('{')
	b = before.find('}')
	temp = before[a+1:b]
	if (not name_to_pid.has_key(temp)):
		return ""
	temp = name_to_pid[temp]
	print "change_id before value "+before
	return before[0:a] + temp + before[b:-1]

def generate_medusascript(filename):
	print filename
	ori_xml = ET.parse(filename)
	input = ori_xml.findall('app/input')
	root = ori_xml.find('app')

	for i in input:
		root.remove(i)
	
	ret_val = []
	x = 0
	for i in input:
		x = x + 1
		tree = copy.deepcopy(ori_xml)
		test = tree.find('app')
		before = i.findtext('gvar')
		if before.find('{') != -1:
			after = change_id(before)
			if (after == ""):
				continue
			i.find('gvar').text = after
		for j in range(len(i)):
			test.insert(0, i[len(i) - j - 1])	
		fname ="program/"+ "%s_%s.xml" % (str(int(time.time())), str(int(random.random()*10000)))
		tree.write(fname)
		ret_val.append([fname, i.findtext('name')])
#`	os.system("rm %s" % filename)
	return ret_val

def savefile(file):
	global CONN,soc
	pair = file.popitem()
	print "pair =  "+pair[1][0]
	if pair[0] == "medusa_rss":
		info = pair[1][0].split(',')
		pid = info[1]
		qid = info[2]
		print "pid qid %s" % str(pid+","+qid)
		msend(CONN[(pid)],pair[1][0])
	else:
		t_filename = "program/%s%s" % (str(int(random.random()*10000)), pair[0])
		f = open(t_filename, 'w')
		x = f.write(pair[1][0])
		f.close()
		filenames = generate_medusascript(t_filename)
		print filenames
		run_medusascript(filenames)


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
	def do_HEAD(s):
		s.send_response(200)
		s.send_header("Content-type", "text/html")
		s.end_headers()
	def do_POST(self):
		ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
		if ctype == 'multipart/form-data':
			postvars = cgi.parse_multipart(self.rfile, pdict)
		elif ctype == 'application/x-www-form-urlencoded':
			length = int(self.headers.getheader('content-length'))
			postvars = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
			savefile(postvars)
		else:
			postvars = {}
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()


if __name__ == '__main__':
	t = ThreadClass()
	t.daemon = True
	t.start()

	server_class = BaseHTTPServer.HTTPServer
	httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
	print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		for d in CONN:
			CONN[d].close()
		soc.close()
		print("Bye~")
		httpd.server_close()
		
	print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
