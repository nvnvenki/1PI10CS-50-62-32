from mobiles import Mobile
import os
import re
from datetime import datetime

#Database object
class Database:
	''' This is the database class which manages the database'''
	def __init__(self):
		'''This is the init method'''
		#This is the database - contains list of dictionaries where key is companyname and value is a list of the mobile objects of that company
		self.database = {}
		self.files = {}


	def populate_db(self , mobiles_list):
		'''This method populates the database
		Parameter is a list of dictionaries'''
		
		mobile_db = [] #list of mobile objects
		for eachMobile in mobiles_list:
			#for each mobile create a object - treating each mobile as an Mobile object
			mob = Mobile()
			mob.name = (eachMobile['company'],eachMobile['model']) #name of the object - something similar to primary key
			mob.specifications = eachMobile #specifications
			if eachMobile not in mobile_db:
				mobile_db.append(mob)
				
		#To separate the mobiles according to companies
		self.__categorise(mobile_db)

	def __categorise(self , mobile_db):
		'''This method categorises the database based on some default convention
		Parameter is a list of mobile objects'''
		#mobile_db  list of objects
		companies_in_db = []
		companies = {}
		files = {}
		try:
			for eachMobile in mobile_db:
				if not companies.has_key(eachMobile.name[0]):
					companies[eachMobile.name[0]] = []
					if not os.path.exists("../Database/" +eachMobile.name[0]):
						os.mkdir("../Database/" +eachMobile.name[0])
					files[eachMobile.name[0]] = open("../Database/" + eachMobile.name[0] + "/" + eachMobile.name[0] + ".txt","w") 
					if eachMobile.name[0] not in companies_in_db:
						companies_in_db.append(eachMobile.name[0])
			companies_in_db.append("all")
			companies_db = open("../Database/" +"companies.txt","w")
			companies_db.write(str(companies_in_db))
			companies_db.close()
		


			for eachMobile in mobile_db:
				companies[eachMobile.name[0]].append(eachMobile)
				files[eachMobile.name[0]].writelines(str(eachMobile.name) +","+ str(eachMobile.specifications) + "\n")

			for eachMobile in mobile_db:
				files[eachMobile.name[0]].close()
			self.database = companies
			self.files = files
		except IOError as exception:
			log = open("../log/log.txt","a")
			log.write(str(datetime.now()) + " | " + exception.message + "File not found!")
			log.close()

	def get_names(self):
		names = []
		for eachCompany in self.database:
			for eachMobile in self.database[eachCompany]:
				names.append(eachMobile.name)
		return names

	def query(self,query_string):
		'''Answers the query'''
		required_data = {}
		'''
		format of required_data
		required_data = {
			'company':'string specifying company - 'all' if to search all company'
			'required_features':[{}] - list of dictionaries key is required features as key value pair like OS:windows
	
 		}
 		'''
 		try:
			if self.__isValidQuery(query_string):
				required_data['company'] = query_string[query_string.find('FROM') + len('FROM') + 1:query_string.find('WITH')].strip()
				required_data['required_features'] = []
				features_list = query_string[query_string.find('W') + 5:].replace(" ","").split('AND')
				
				companies_list = eval(open("../Database/companies.txt").read())
				
				
				if required_data['company'] in companies_list:
					for eachFeature in features_list:
						#print eachFeature
						if '=' in eachFeature:
							operator = '='
						elif '>' in eachFeature:
							operator = '>'
						elif '<' in eachFeature:
							operator = '<'
						feature_details = {}
						temp = eachFeature.split(operator)
						feature_details[temp[0]] = operator + temp[1]
						#print feature_details
						required_data['required_features'].append(feature_details)
					#print required_data
					
					self.__answer_query(required_data)

				else:
					print "The company u r looking for is not found"
					raise Exception("The company u r looking for is not found")
				 		
			else:
				print "Invalid query!!"
				raise Exception("Invalid Query")
		
		except Exception as exception:
			log = open("../log/log.txt","a")
			
			log.write(str(datetime.now()) + " | " + query_string + " | " + exception.message + "\n")
			log.close()

	def __isValidQuery(self,query_string):
		'''Validates the query'''
		#SELECT mobiles FROM Samsung WITH operatingsystem = windows

		regex1 = "SELECT mobiles FROM (\w*) WITH "
		regex2 = "(operatingsystem|talktime|type|GPS|price|rearcamera|frontcamera|thickness|company) (=|>|<) (\w*)"

		query_pattern = regex1 + regex2 +"( AND " + regex2 + ")*"
		# print query_pattern
		m = re.match(query_pattern,query_string)
		if m:
			return True
		else:
			return False


	def __answer_query(self,required_data):
			'''
				this answers to the query based on the metadata obtained from parsing
				have to handle the exceptions in this func as the company name requested may not be found in the file system
			'''
			selected_mobiles = []
			
			mobile_info = []
			company = required_data['company'].strip()
			companies_list = eval(open("../Database/" +"companies.txt").read())
			
			
			if company != "all":
				db_file = open("../Database/" + company + "/" + company + ".txt")
				 #this is a list of tupples => (key,specifications)
				for eachLine in db_file:
					mobile_info.append(eval(eachLine)[1])
			else:
				#companies_list = eval(open("companies.txt").read())
				companies_list.remove("all")
				for eachCompany in companies_list:
					db_file = open("../Database/" +eachCompany + "/" + eachCompany + ".txt")
				    #this is a list of tupples => (key,specifications)
					for eachLine in db_file:
						mobile_info.append(eval(eachLine)[1])

					db_file.close()
				
			del required_data['company']
				
			for eachFeatureRequired in required_data.keys():
					features = required_data[eachFeatureRequired]
					for eachMobile in mobile_info:
						num = []
						for eachFeature in features:
							info = eachFeature.items()
							key , value = info[0][0],info[0][1]
							if eachMobile.has_key(key):
								operator = value[0]
								value = value[1:]
								if value.isdigit():
									value = int(value)
								left = eachMobile[key]
								if left.isdigit():
									left = int(left)
								if operator == '=':
									num.append(left == value)
								elif operator == '>':
									num.append(left > value)
								elif operator == '<':
									num.append(left < value)
						
						flag = reduce(lambda x, y:x and y,num)
						if flag:
							selected_mobiles.append( company + ":" + str(eachMobile))

			self.__show_result(selected_mobiles)
			
			
	def __show_result(self,selected_mobiles):
		'''displaying result set'''

		if len(selected_mobiles) == 0:
			print "No mobile is found with the given features in the database!"
			
		else:
			f = open("../Answer/results.txt","w")
			f.close()
			keys = eval(selected_mobiles[0][selected_mobiles[0].find("{"):]).keys()
			for eachMobile in selected_mobiles:
				#print eachMobile
				eachMobile = eachMobile[eachMobile.find("{"):]
				_dict = eval(eachMobile)
				self.__format(_dict,keys)



	def __format(self,_dict,keys):
		'''formatting the output'''
		
		buffer_file = open("../Answer/results.txt","a")
		buffer_file.writelines('-' * 110 + '\n')
		for key in keys:
			if _dict[key] == '':
				buffer_file.writelines(key.ljust(20) + ":no" + '\n')
			else:
				buffer_file.writelines(key.ljust(20) + ":" + _dict[key] + '\n')
		buffer_file.writelines('-' * 110 + '\n')
		buffer_file.close()



