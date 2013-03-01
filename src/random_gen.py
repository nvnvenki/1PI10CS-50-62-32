'''This module is used to generate random input data from the predefined lists of data'''
from random import randint

companies = ['Nokia','Samsung','Lg','SonyEricsson','BlackBerry']
types = ['smartphone','basic']
operating_systems = ['windows','android','bada','symbian','blackberry','s40']
input_method = ['keypad','touch']
GPS = ['yes','no']
model = ['lumia','hero','blackberry','N','hero']

def main():
	input_file = open("../Sampleinput/input_file_2.txt","w")

	i = 0
	while i < 4000:
		mobile = {}
		mobile['company'] = companies[randint(0,len(companies) - 1)]
		mobile['type'] = types[randint(0,len(types) -1 )]
		mobile['model'] = model[randint(0,len(model) - 1)] + str(randint(100,4576))
		mobile['price'] = str(randint(1000,40000))
		mobile['operatingsystem'] = operating_systems[randint(0,len(operating_systems) - 1)]
		mobile['frontcamera'] = str(randint(0,20))
		mobile['rearcamera'] = str(randint(0,5))
		mobile['GPS'] = GPS[randint(0,len(GPS) - 1)]
		mobile['talktime'] = str(randint(5,30))
		mobile['thickness'] = str(randint(10,30))
		input_file.writelines(str(mobile) + "\n")
		#print mobile
		i = i + 1		



if __name__ == '__main__':
	main()