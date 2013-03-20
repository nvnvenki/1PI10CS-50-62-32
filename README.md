<h1>Mobile Device database engine.</h1>
<p>
This is the Python project.Mobile Device database engine implemented in python using in memory database. 
<pre>
	
		-commands    : save - to load the data to the database
					 : query - to query the database
					 : close - to close the connection with the server
	
 <h4> Query format: </h4>
  	<hr />
	  - SELECT mobiles FROM 'company' WITH 'features'
	  - conditions:
	     - Companies can be any company.To search in all the companies give company name as 'all'
	     - Features must be specified as follows \n \t feature operator value
	     - WITH clause is mandatory
	     - To get multiple the info of mobile with two or more features seperate each feature with an 'AND'
	     - Operators supported : '=', '&lt;', '&gt;'
	    - features list 
					- operatingsystem
					- price
					- frontcamera
					- rearcamera
					- model
					- thickness
					- talktime
					- GPS 
					- type
					
	
	To check for the existence give 00mp for camera specifications
	Example query:
	Say a user wants to get the info of samsung mobiles with windows os and price less than 10000Rs and with GPS and with rearcamera
	 The query will be
		
		 SELECT mobiles FROM Samsung WITH operatingsystem = windows and cost &lt; 10000 AND GPS = yes AND rearcamera &gt; 0 
</pre>		

</p>
