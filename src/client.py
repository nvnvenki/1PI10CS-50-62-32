import socket
import sys

def main():
	print "-" * 110
	print " " * 40 + "Mobile database"
	print "-" * 110
	print """
			-commands: save - to load the data to the database
					 : query - to query the database
					 : close - to close the connection with the server
							Query format:
			- SELECT mobiles FROM 'company' WITH 'features'
			- conditions:"
			   - Companies can be any company.To search in all the companies give company name as 'all'
			   - Features must be specified as follows 
			   			'feature' operator 'value'

			   - WITH clause is mandatory
			   - To get multiple the info of mobile with two or more features seperate each feature with an 'and'
			   - Operators supported : '=', '<', '>'"
			- features 
					* operatingsystem ( only operator '=' must be used )
					* price
					* frontcamera
					* rearcamera
					* thickness
					* talktime
					* GPS ( only operator '=' must be used )
					* type ( only operator '=' must be used )

	
	Say a user wants to get the info of samsung mobiles with windows os and price less than 10000Rs and with GPS and with rearcamera\n \t The query will be
	\t\t SELECT mobiles FROM Samsung WITH operatingsystem = windows and price < 10000 and GPS = yes and rearcamera > 0"""
	print "-" * 110

	try:
		socket_ = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #TCP socket to the server
		host = socket.gethostname() #get the local machine name
		port = 12345 #Server port

		print "Connecting to database server ",host," to the port ",port
		socket_.connect((host,port))
		last_command = "query"
		while True:
			message = raw_input("command>>")
			last_command = message
			if last_command != "query" and message not in ['save','query','close']:
				print "Invalid command"
				continue
			if last_command == "query":
				message = raw_input("query>>")
				if message in ['close','save','query']:
					print "Invalid command"
					continue
				f = open("../Answer/client.txt","w")
				f.close()
				socket_.send(message)
				with open("../Answer/client.txt","a",0) as fobj:
					line = socket_.recv(1024)
					while 'close' not in line:
						fobj.write(line)
						line = socket_.recv(1024)
					print "here"
				fobj.close()
				continue
				
			if last_command == "save":
				socket_.send(message)
				print "Loading data into the database..please wait"
				message = socket_.recv(1025)
			
				message = eval(message)
				print "response>>",message[0]
				if message[1] == 0:
					socket_.close()
					sys.exit()
				continue
			if last_command == "close":
				print "terminating connection"
				socket_.close()
				sys.exit()
			

	except Exception:
		print "Something went wrong!"
		print Exception.message;

if __name__ == '__main__':
	main()