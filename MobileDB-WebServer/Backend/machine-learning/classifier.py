#! usr/bin/python
# filename : classifier.py
import Orange
import pymongo
import ast
import json

def main():
	#to establish the connection with the mongo database
	connection = pymongo.MongoClient("localhost",27017)
	database = connection["device_database"]
	collection = database["devices"]

	#load the training set and get the classifier object of Orange
	data = Orange.data.Table("training_set")
	learner = Orange.classification.bayes.NaiveLearner()
	classifier = learner(data)
	'''
	#testing
	for d in data[:5]:
		class_ = classifier(d)
		print "%-10s..... originally....%-10s" % (class_,d.getclass())

	'''
	#finding all the possible keys
	keys_list = []
	cursor = collection.find({"Company":"Nokia"})
	for device in cursor:
		device.pop("_id")
		device = ast.literal_eval(json.dumps(device).encode("ascii","ignore"))
		keys_list.extend(device.keys())
	keys_list = list(set(keys_list))
	keys_list.append('segment')

	#since i am using Orange as a machine learning tool, the input file should conform to a specific format. which is
	#first line : attribute names
	#second line: defining their types either discrete or continuous
	#third line : for specifying a class attribute

	#Lets add the classified details to a new collection : devices_classified
	classified_collection = database['classified_devices']

	#checking the classifier working!!!
	cursor = collection.find({'Company':'Apple'})
	for device in cursor:
		_id = device.pop("_id")
		device = ast.literal_eval(json.dumps(device).encode("ascii","ignore"))
		attr_vals = []
		fobj = open("temp_file.tab","w")
		fobj.write("\t".join(keys_list) + "\n")
		fobj.write("\t".join(['d'] * len(keys_list)) + "\n")
		cls = [''] * len(keys_list)
		cls[-1] = 'class'
		fobj.write("\t".join(cls) + "\n")
		for key in keys_list:
			if not device.has_key(key):
				attr_vals.append("No")
			else:
				attr_vals.append(str(device[key]))
		fobj.write("\t".join(attr_vals) + "\n")
		fobj.close()
		#segmented document :D	
		# print len(open('temp_file.tab').read().strip().split('\n'))
		# print type(Orange.data.Table('temp_file.tab'))
		class_ = classifier(Orange.data.Table("temp_file.tab")[0])
		
		device['segment'] = (str(class_).decode("ascii","ignore")).encode("ascii")
		classified_collection.insert(device)
		print "Mobile:" , device['Brand'],"Class : ",class_
		# print "price :\t%-10d class :\t%-10s" % (device["Price group"],class_)

if __name__ == '__main__':
	main()
