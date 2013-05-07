#! usr/bin/python
# filename : classifier.py
import pymongo
import ast
import json
import re


def main():
	#to establish the connection with the mongo database
	connection = pymongo.MongoClient("localhost",27017)
	database = connection["device_database"]
	collection = database["devices"]

	#find all the keys in a collection
	keys_list = []
	cursor = collection.find({"Company":"Apple"})
	for device in cursor:
		device.pop("_id")
		device = ast.literal_eval(json.dumps(device).encode("ascii","ignore"))
		keys_list.extend(device.keys())
	keys_list = list(set(keys_list))
	keys_list.append('segment')

	#open a file training_set.tab and write the corpus to it.
	open("training_set.tab","w").close()
	
	fobj = open("training_set.tab","a")

	#since i am using Orange as a machine learning tool, the input file should conform to a specific format. which is
	#first line : attribute names
	#second line: defining their types either discrete or continuous
	#third line : for specifying a class attribute

	#first line
	fobj.write("\t".join(keys_list) + "\n")

	#second line
	fobj.write("\t".join(['d'] * len(keys_list)) + "\n")

	#third line 
	cls = [''] * len(keys_list)
	cls[-1] = 'class'
	fobj.write("\t".join(cls) + "\n")

	#now create a training set bases upon the input device attribute values
	cursor = collection.find()
	for device in cursor:
		_id = device.pop("_id")
		device = ast.literal_eval(json.dumps(device).encode("ascii","ignore"))
		
		#initialise the type
		smart_phone = False
		high_end = False
		low_end = False
		mid_range = False

		smart_pattern = r'(?i).*?(Android|Windows|iOS|Black Berry).*?'
		
		#is it a smart phone ? finding based on OS's
		if device.has_key("OS"):
			robj = re.match(smart_pattern,device["OS"])
			if robj:
				smart_phone = True

		#is it a high end or mid range or low end phone? finding based on the price as well as if its a smart phone
		if device.has_key("Price group"):
			if (smart_phone and device["Price group"] >= 300) or (device["Price group"] >= 300):
				high_end = True
			elif (smart_phone and device["Price group"] < 300) or (not smart_phone and device["Price group"] >= 100):
				mid_range = True
			elif (not smart_phone and device["Price group"] < 100) or (device["Price group"] < 100):
				low_end = True
		#find the values to insert to training set for this device
		attr_vals = []
		for attr in keys_list[0:-1]:
			if device.has_key(attr):
				attr_vals.append(str(device[attr]))
			else:
				attr_vals.append("No")
		if high_end:
			attr_vals.append("high_end")
		elif mid_range:
			attr_vals.append("mid_range")
		elif low_end:
			attr_vals.append("low_end")
		fobj.write("\t".join(attr_vals) + "\n")	
if __name__ == '__main__':
	main()