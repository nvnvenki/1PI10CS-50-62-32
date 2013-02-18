from db import Database

def main():
	file_name = '../Sampleinput/input_file.txt'
	db_file = open(file_name)
	mobiles_list = []
	for eachLine in db_file:
		mobiles_list.append(eval(eachLine))
	db_file.close()
	#create a database object
	database = Database() 
	database.populate_db(mobiles_list)
	
	print "-" * 110
	print " " * 40 + "Mobile database"
	print "-" * 110
	print "Query format:"
	print "  - SELECT mobiles FROM 'company' WITH 'features'"
	print "  - conditions:"
	print "     - Companies can be any company.To search in all the companies give company name as 'all'"
	print "     - Features must be specified as follows \n \t feature operator value"
	print "     - WITH clause is mandatory"
	print "     - To get multiple the info of mobile with two or more features seperate each feature with an 'and'"
	print "     - Operators supported : '=', '<', '>'"
	print """    - features list 
					* operatingsystem
					* price
					* frontcamera
					* rearcamera
					* model
					* thickness
					* talktime
					* GPS 
					* type """

	print "To check for the existance give 00mp for camera specifications"
	print "Example query:"
	print "Say a user wants to get the info of samsung mobiles with windows os and price less than 10000Rs and with GPS and with rearcamera\n \t The query will be"
	print "\t\t SELECT mobiles FROM Samsung WITH operatingsystem = windows and cost < 10000 and GPS = yes and rearcamera > 00mp"
	print "-" * 110
	
	yes = raw_input("Do you want to enter the query?? y/n \n")
	if(yes == "y"):
		print "-" * 110
		start = True	
		while start:
			query_string = raw_input("Enter the query\n")
			print "-" * 110
			database.query(query_string)
			print "-" * 110
			continue_ = raw_input("Want to give next query?? y/n \n")
			if continue_ != "y":
				start = False 	 
				
		print "-" * 110
		print "Thank You!"
	else:
		print "-" * 110
		print "Thank you!"

	except Exception as exception:
if __name__ == '__main__':
	main()
