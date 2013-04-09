import socket
import threading
from db import Database

def process_request(client,address):
	database = Database()
	
	while True:
		message = client.recv(1025)
		if message == "close":
			client.send(str(("Thanks for using this database!",0))) # second parameter is 0 - indicates that the client should terminate now like a status
			break;
		elif message == "save":
			file_name = '../Sampleinput/input_file.txt'
			db_file = open(file_name)
			mobiles_list = []
			for eachLine in db_file:
				mobiles_list.append(eval(eachLine))
			db_file.close()
			#client.send(str(("Saving data into the database! Please wait...",1)))
			database.populate_db(mobiles_list)
			client.send(str(("Database is saved!!",1)))
		else:
			database.query(message)
			with open("../Answer/results.txt","r",0) as fobj:
				line = fobj.read(1024)
				while line:
					client.send(line)
					line = fobj.read(1024)
				client.send('close')
			print "sending complete"

	client.close()



def main():
	try:
		socket_ = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # TCP socket
		host = socket.gethostname() #host name
		port = 12345 # port number

		print "Server started!"
		socket_.bind((host,port))
		socket_.listen(5)
		
			
		while True:
			print "Waiting for client"
			client , address = socket_.accept()
			print "Got a connection from ",address
			thread = threading.Thread(target = process_request,args=(client,address))
			thread.start()
		
	except Exception:
		print "Something went wrong!" + str(Exception.message)
	finally:
		socket_.close()

if __name__ == '__main__':
	main()