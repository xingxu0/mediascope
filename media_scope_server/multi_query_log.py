import time, os, copy, sys, random, threading, errno, datetime, copy, operator
import BaseHTTPServer, urlparse, cgi,urllib, urllib2, multi_query_lib
from urllib2 import Request, urlopen, URLError, HTTPError
from googlemaps import GoogleMaps
from threading import Thread

#HOST_NAME = '98.148.179.148'
#HOST_NAME = '127.0.0.1'
HOST_NAME = '128.125.121.187'
#HOST_NAME = '192.168.1.142'
HOST_PORT = 8080 
PORT_NUMBER = 9000

active_queries = {'0' : 'Empty Query Set'}
pending_task = {}
pending_photo = {}

cs_dbhost = "tomography.usc.edu"
cs_dbname = "aqua"

arriving_time = {}
uploading_time = {}

Uploaded  = {}
SPD = {}
TM = {}

log_file = open("log/log_file", "wa")


def getfile(fl):
	global Uploaded, SPD, TM
	time_log = threading.local()
	time_log.s = ''
	time_log.s += str(time.time()) + "\t(Y)notifiction received \r\n"	
	flag = 0
	pair = fl.popitem()
	#print "pair =  "+pair[1][0]
	#t_filename = "%s%s" % (str(int(random.random()*10000)), pair[0])
	if pair[0] != '':
		#print pair[0]
		name_uids = pair[0].split('=')
		uids = name_uids[1].split('|')
		for i in range(len(uids)):
			download_urls = pair[1][0].split(",")
		con, cur = sql_execute2()
		for i in range(len(download_urls)):
			download_url = download_urls[i]
			#print download_url 
			filename = name_uids[0]+'='+uids[i]#+'='+name_uids[-1] 
			ext = download_url.split('.')[-1]
			download_url = "http://"+download_url 
			
			if ext == 'txt':
				filename = './meta/' + filename
				urllib.urlretrieve(download_url, filename)
				f = open(filename, 'r')
				line = f.readline()
				if line[:4] != 'none':
					sql_in = "INSERT INTO Meta_data (user, uid, feature, longtitude, latitude, time, size ) VALUES (" + line[:-1] +");"
					#print sql_in
				#	con, cur = sql_execute(sql_in)
					cur.execute(sql_in)
					line = f.readline()
					while line:
						sql_in = "INSERT INTO Meta_data (user, uid, feature, longtitude, latitude, time, size ) VALUES (" + line[:-1] +");"
						#print sql_in
						cur.execute(sql_in)
						line = f.readline()
				#	con.close()
				f.close()
			else:
				flag = 1
								
				ffilename = './query/'+filename
#				sql_get = ("select size from Meta_data where user = {0} and uid = {1}").format(name.uids[0], uids[i])
#				cur.execute(sql_get)
#				dat = cur.fetchone()
				urllib.urlretrieve(download_url, ffilename)
				#SIZE = 0
				print "Got file " + filename
				temp = filename.split('=')
				if (not uploading_time.has_key(temp[0])):
					arriving_time[temp[0]] = {}
					uploading_time[temp[0]] = {}
				if (len(arriving_time[temp[0]]) == 0):
					v = 0
				else:
					(k, v) = max(arriving_time[temp[0]].iteritems(), key=operator.itemgetter(1))
				arriving_time[temp[0]][temp[1]] = time.time()
				uploading_time[temp[0]][temp[1]] = arriving_time[temp[0]][temp[1]] - v
				log_file.write(filename + " " + str(uploading_time[temp[0]][temp[1]]) + " " + str(datetime.datetime.utcfromtimestamp(int(time.time() - 7*3600))) +"\r\n")
				log_file.flush()
				
				sql_up = ("update Meta_data set size = 0 where user = {0} and uid = {1}").format(name_uids[0],uids[i])
				#print sql_up
#				cur.execute(sql_up)
				#time_log.s += str(time.time()) + "\t(Y)fetched {0} \r\n".format(filename)
		con.close()
	else:
		print 'No photo captured!'
		pass
	if flag == 1:
		pass
		#mdlib.update_program_state(cs_dbhost, cs_dbname, "yx_server", "time", time_log.s)	

def sql_execute2():
	import MySQLdb as mdb
	con = None
	data = None
	host = "localhost"
	dbname = "medusa"
	try:
		con = mdb.connect(host, 'root', 'xx', dbname)
		cur = con.cursor()
		#cur.execute(sqlstmt)
	except mdb.Error, e:
		#log("! get_raw_mysql_data() err %d: %s" % (e.args[0], e.args[1]))
		print "sql_execute error"
	return con, cur

def sql_execute( sqlstmt):
	import MySQLdb as mdb
	con = None
	data = None
	host = "localhost"
	dbname = "medusa"
	try:
		con = mdb.connect(host, 'root', 'xx', dbname)
		cur = con.cursor()
		cur.execute(sqlstmt)
	except mdb.Error, e:
		#log("! get_raw_mysql_data() err %d: %s" % (e.args[0], e.args[1]))
		print "sql_execute error"
	return con, cur
	
class FileHandler(threading.Thread):
	def run(self):
		getfile(self.fl)
	def __init__(self, fl):
		threading.Thread.__init__(self)
		self.fl = fl

class YXMyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
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
			#print postvars
			t = FileHandler(postvars)
			t.start()
#			getfile(postvars)
		else:
			postvars = {}
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()


def yx_server_thread():
    	server_class = BaseHTTPServer.HTTPServer
	httpd = server_class((HOST_NAME, PORT_NUMBER), YXMyHandler)
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass

	httpd.server_close()

# =================== below multi_query.py ======================


def kill_users(users):
        f = open('kill_xml','r')
        kill_xml_file = ''

        for user, pending_list in users.iteritems():
                task_id = "KILL_STAGE_" + multi_query_lib.unique_id()
                kill_xml_file += multi_query_lib.generate_task_file(task_id, user, "{"+pending_list[0]+"}")
                kill_xml_file += f.read()
                if multi_query_lib.send_task([('c2dm_upload.xml', kill_xml_file)]) == -1:
			print "Send kill task failed"
        print "kill: "+str(users)

def accept_query(qid, paras):
        global pending_photo, pending_task
        pending_task[qid] = {}
	pending_photo[qid] = {}
	
	(result, meta) = multi_query_lib.select(paras)
        print "query_result = "+str(result)
        #print "meta = "+str(meta)
        if (len(result)) == 0:
                return
        f = open('upload_xml','r')
	upload_xml_file = ''

	for user in result:
                task_id = "PHOTO_UPLOAD_" + multi_query_lib.unique_id()
		#print "=="+str(user)+str(result[user])
                upload_xml_file += multi_query_lib.generate_task_file(task_id, user, result[user])
		pending_task[qid][user] = [] 
                pending_task[qid][user].append(task_id)
                uids = result[user].split('|')
                #metas = meta[user].split('|')
                for i in range(len(uids)):
			only_uid = uids[i].split(':')
                        pending_task[qid][user].append(only_uid[0])
                        pending_photo[qid][user + '=' + only_uid[0]] = int(only_uid[1])
        upload_xml_file += f.read()
        if multi_query_lib.send_task([('c2dm_kill.xml', upload_xml_file)]) == -1:
		print "Send upload task failed"	
        print "Pending photos: "+str(pending_photo)
        print "Pending tasks: "+str(pending_task)

def return_result(qid, q_type):
	global pending_photo, pending_task, active_queries, arriving_time, uploading_time
	
	#print "ARRIVING: " + str(arriving_time)
	#print "UPLOADING_TIME: " + str(uploading_time)
	
	temp_pending_photo = copy.deepcopy(pending_photo)
	for k,v in pending_photo[qid].iteritems():
        	if (os.path.exists('query/' + k)):
                        names = k.split('=')
                        pending_task[qid][names[0]].remove(names[1])
                        if (len(pending_task[qid][names[0]]) == 1):
                        	del pending_task[qid][names[0]]
	if len(pending_task[qid]) > 0:
		kill_users(pending_task[qid])
	
	ret_val = ''
	if (len(pending_photo[qid]) == 0):
        	ret_val += "<h2>No relevent results.</h2>"
 	        del pending_photo[qid]
		del pending_task[qid]
		del active_queries[qid]
		return ret_val
	if (q_type[0] == '0'):
		ret_val += "Query Object: <br> </br><img src=\"data:image/jpg;base64,{0}\" width=205><br> </br>".format(open('QUERY_IMAGE/' + q_type[1:]).read().encode('base64').replace('\n', ''))

        ret_val += 'Result Objects: <br> </br> <table border=1 bordercolor=#999999 width=600><tr>'

        gmaps = GoogleMaps()
	while (len(pending_photo[qid]) > 0):
		(k, v) = max(pending_photo[qid].iteritems(), key=operator.itemgetter(1))
        	temp = k.split('=')
                ret_val += "<td width=205>"
                if (os.path.exists('query/' + k)):
                	ret_val += "<img src=\"data:image/jpg;base64,{0}\" width=205>".format(open('query/' + k).read().encode('base64').replace('\n', ''))
                else:
                	ret_val += "<b>Warning:</b> Photo failed to be uploaded on time."
                #temp = v.split(',')
                #dd = datetime.datetime.fromtimestamp(long(temp[len(temp) - 2])/1000)
                #tt = dd.isoformat(' ')
                #destination = "a, b, c, d, e, f, g"
                #destination = gmaps.latlng_to_address(float(temp[3]), float(temp[2]))
                #dest = destination.split(', ')
                #ret_val += "<p><b><pre>Location: </b>{0}</pre></p>".format(dest[0])
		ret_val += "<p><b><pre>Credit: </b>{0}</pre></p>".format(str(pending_photo[qid][k]))
                #del dest[0]
                #dest[-2] += ', ' + dest[-1]
                #del dest[-1]
   		#for dests in dest:
                #	ret_val += "<p><pre>            {0}</pre></p>".format(dests)
		ret_val += "<p><b><pre>Name: </b>{0}</pre></p>".format(k)
		del pending_photo[qid][k]
	ret_val += "</td>"
        del pending_photo[qid]
	del pending_task[qid]
	del active_queries[qid]
        print 'Finish response to ('+str(qid)+'). '
	print '    Now query set (' + str(active_queries)+')'
	print '    Pending photo ('+str(pending_photo)+')'
	print '    Pending task ('+str(pending_task)+')'
	print "    UPLOADING_TIME (" + str(uploading_time)+')'
	return ret_val


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
	def do_HEAD(s):
		s.send_response(200)
		s.send_header("Content-type", "text/html")
		s.end_headers()
	def do_GET(self):
		url_content = urlparse.urlparse(self.path)
		query = url_content.query
		path = url_content.path
		if path != "/medusa":
			return
		args = query.split("&")
		paras = {}
		for i in range(len(args)):
			temp = args[i].split("=")
			if len(temp) >= 2:
				paras[temp[0]] = temp[1]
	        self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()
		self.wfile.write("<html><body>")
#		self.wfile.write("Query is: " + str(paras)+"\r\n")
		if 'query_id' in paras:
			self.wfile.write(return_result(paras['query_id'], paras['type']+paras['option2']))
		else:
			query_id = str(int(max(active_queries)) + 1)
			#print "accepted query (" + str(query_id)+")"
			active_queries[query_id] = query
			accept_query(query_id, paras)
			self.wfile.write("<Meta http-equiv=\"Refresh\" Content=\"" + paras['deadline'] + "; url=http://" + HOST_NAME + ":" + str(HOST_PORT) + "/medusa?" + query + "&query_id=" + query_id + "\">")
		self.wfile.write("</body></html>")		

if __name__ == '__main__':
	
	t = Thread(target=yx_server_thread, args=())
	t.start()

	server_class = BaseHTTPServer.HTTPServer
	httpd = server_class((HOST_NAME, HOST_PORT), MyHandler)
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass
	
	t.join(0)
	print "Writting log..."
	httpd.server_close()
	logfile = "log/log_"+str(time.time())
	f = open(logfile, 'w')
	f.write(str(arriving_time))
	f.write(str(uploading_time))
	f.flush()
	f.close()
	os._exit(0)
