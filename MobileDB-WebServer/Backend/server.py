#! use/bin/python
#filename : basic_http_server

from datetime import datetime
import BaseHTTPServer
import cgi
import json
import pymongo
import ast
import sample

# logfile = open("logs/log.txt","a")

class myHandler(BaseHTTPServer.BaseHTTPRequestHandler):
   def do_HEAD(s):
      s.send_response(200)
      s.send_header("Content-Type","text/html")
      s.end_headers()
   def do_POST(s):
      # print "Hi in post"
      logfile = open("logs/log.txt","a")
      # s.logfile.close()
      json_obj = s.rfile.read(int(s.headers['Content-Length']))
      json_obj = eval(json_obj)
      print json_obj
      if json_obj.has_key('type'):
         if json_obj['type'] == 'signin':
            res = signin(json_obj,logfile)
            # s.logfile.write(" | Signin time: " + str(datetime.now()))
         elif json_obj['type'] == 'signup':
            res = signup(json_obj,logfile)
         elif json_obj['type'] == 'query':
            res = query_handle(json_obj,logfile)
      s.send_response(200)
      s.send_header("Access-Control-Allow-Origin","*")
      s.send_header("Content-Type:","application/json; charset=UTF-8")
      s.end_headers()
      # s.logfile.close()
      s.wfile.write(res)
   def do_GET(s):
      fields = cgi.FieldStorage(fp=s.rfile,headers=s.headers,environ={'REQUEST_METHOD':'POST','CONTENT_TYPE':s.headers['Content-Type']})
      name = fields.getfirst('name')
      s.send_response(200)
      s.send_header("Access-Control-Allow-Origin","*")
      s.send_header("Content-Type:","application/json; charset=UTF-8")
      s.end_headers()
      d = {
         'name':name.upper(),
         'sem':'6'
      }
      s.wfile.write(json.dumps(d))
def signin(json_obj,logfile):
      client = pymongo.MongoClient('localhost',27017)
      database = client['device_database']
      collection = database['auth']
      user_name = json_obj['username']
      password = json_obj['password']
      cursor = collection.find({'username':user_name,'password':password})
      if cursor.count():
         logfile.write("signin from\t" + user_name + "\twas successful at\t" + str(datetime.now()) + "\n")
         logfile.close()
         return '{"status":"True"}'
      else:
         logfile.write("signin from\t" + user_name + "\twas unsuccessful at\t" + str(datetime.now()) + "\n")
         logfile.close()
         return '{"status":"False"}'
def signup(json_obj,logfile):
      client = pymongo.MongoClient('localhost',27017)
      database = client['device_database']
      collection = database['auth']
      
      json_obj.pop('type')

      user_name = json_obj['username']

      cursor = collection.find({'username':user_name})
      if cursor.count():
         client.close()
         logfile.write("signup from\t" + user_name + "\twas successful at\t" + str(datetime.now()) + "\n")
         logfile.close()
         return '{"status":"False"}'
      else:
         collection.insert(json_obj)
         client.close()
         logfile.write("signup from\t" + user_name + "\twas unsuccessful at\t" + str(datetime.now()) + "\n")
         logfile.close()
         return '{"status":"True"}'
def query_handle(json_obj,logfile):
      client = pymongo.MongoClient('localhost',27017)
      database = client['device_database']
      collection = database['devices']

      json_obj.pop('type')
      
      print json_obj

      li = []
      print json_obj

      print type(json_obj)

      mongo_query = sample.get_mongo_query(json_obj['query'])
      if mongo_query[0] == True:
         if len(mongo_query[1]) > 1:
               peeps =  collection.find(mongo_query[1][0],mongo_query[1][1])
         else:
               peeps =  collection.find(mongo_query[1][0])
         #cursor = collection.find(eval(json_obj['query']))
         #print cursor.count()
         for elem in peeps:
            _id = elem.pop('_id')
            li.append(ast.literal_eval(json.dumps(elem)))
         # print li[0]
         logfile.write("query handling was successful at\t" + str(datetime.now()) + "\n")
         logfile.close()
         return '{"result":"' + str(li) + '","valid_query":"True"}'
      else:
         logfile.write("query handling was unsuccessful at\t" + str(datetime.now()) + "\n")
         logfile.close()
         return '{"valid_query":"False"}'
def main():
   server_class = BaseHTTPServer.HTTPServer
   httpd = server_class(('',80),myHandler)
   try:
      httpd.serve_forever()
   except KeyboardInterrupt,e:
      print e.message
   finally:
      httpd.server_close()
if __name__ == '__main__':
   main()
