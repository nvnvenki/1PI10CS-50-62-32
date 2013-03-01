Mobile database:
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

	Example query:
	Say a user wants to get the info of samsung mobiles with windows os and price less than 10000Rs and with GPS and with rearcamera
	 The query will be
	
		 SELECT mobiles FROM Samsung WITH operatingsystem = windows and cost < 10000 and GPS = yes and rearcamera > 0