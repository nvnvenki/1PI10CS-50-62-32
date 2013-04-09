#! use/bin/python
#filename : basic_http_server

import BaseHTTPServer
import string
import sdk

class myHandler(BaseHTTPServer.BaseHTTPRequestHandler):
	def do_HEAD(s):
		s.send_response(200)
		s.send_header("Content-Type","text/html")
		s.end_headers()
	def do_GET(s):
		s.send_response(200)
		s.send_header("Content-Type","text/html")
		s.end_headers()
		s.wfile.write(open("./touch_enabled.html","r").read())
		header_info = s.headers
		string_format = str(header_info)
		user_agent = extract_user_agent(string_format)
		print get_response(user_agent)
def extract_user_agent(header):
	info_list = string.split(header,'\n')
	info_dict = {}
	for info in info_list:
		if info:
			temp = info.split(':')
			info_dict[temp[0]] = temp[1]
	user_agent = info_dict.get('User-Agent')
	print user_agent.strip()
	return user_agent.strip()
def get_response(user_agent):
	sdk.isTouch(user_agent)

def main():
	server_class = BaseHTTPServer.HTTPServer
	httpd = server_class(('',80),myHandler)
	try:
		httpd.serve_forever()
	except KeyboardInterrupt,e:
		print e.message
	httpd.server_close()
if __name__ == '__main__':
	main()
