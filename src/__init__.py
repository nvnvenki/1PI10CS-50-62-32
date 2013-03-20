from db import Database

def main():
	print "-" * 110
	print " " * 40 + "Mobile database"
	print "-" * 110
	print """						Query format:
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

	
	
	start = True
	database = Database()
	while start:
		print "-" * 110
		print """					Menu"""
		print "-" * 110
		print """
				1.Save the new data into database
				2.Query the database
				3.Exit
			  """
		print "-" * 110

		choice = raw_input("Enter the choice!\n")
		if choice == '1':
			file_name = '../Sampleinput/input_file.txt'
			db_file = open(file_name)
			mobiles_list = []
			for eachLine in db_file:
				mobiles_list.append(eval(eachLine))
			db_file.close()
			print "Saving data into the database! Please wait..."
			database.populate_db(mobiles_list)
			print "Database is saved!!"
		elif choice == '2':
			query_string = raw_input("Enter the query\n")
			print "-" * 110
			database.query(query_string)
			print "-" * 110
		elif choice == '3':
			start = False
		else:
			print "Invalid choice"

if __name__ == '__main__':
	main()
