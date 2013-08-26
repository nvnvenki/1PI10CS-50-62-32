<h1>Mobile Device database engine.</h1>
<p>
This is the Python project.Mobile Device database engine implemented in python using in memory database. 
<p>
	
		-commands    : save - to load the data to the database
					 : query - to query the database
					 : close - to close the connection with the server
	
 <h4> Query format: </h4>
  	<hr />
  	<ul>
  	
	  <li> SELECT mobiles FROM 'company' WITH 'features' </li>
	  <li>conditions: </li>
	  	<li><ul>
	     <li> Companies can be any company.To search in all the companies give company name as 'all'</li>
	     <li> Features must be specified as follows \n \t feature operator value</li>
	     <li> WITH clause is mandatory</li>
	     <li>To get multiple the info of mobile with two or more features seperate each feature with an 'AND'</li>
	     <li> Operators supported : '=', '&lt;', '&gt;'</li>
	    <li>features list <ul>
					<li> operatingsystem</li>
					<li>price</li>
					<li> frontcamera</li>
					<li> rearcamera</li>
					<li> model</li>
					<li> thickness</li>
					<li> talktime</li>
					<li> GPS </li>
					<li> type</li>
					</ul></li>
		</ul></li>			
	</ul>
	<p>To check for the existence give 00mp for camera specifications
	Example query:
	Say a user wants to get the info of samsung mobiles with windows os and price less than 
		<br>10000Rs and with GPS and with rearcamera
	 The query will be
		
		 SELECT mobiles FROM Samsung WITH operatingsystem = windows and cost &lt; 10000
		<br>AND GPS = yes AND rearcamera &gt; 0 
	<p> <a href="pymobileinfo.appspot.com">Site </a>
		<img src="https://dl.dropboxusercontent.com/u/109288873/pymobile.png"></p></p>
</p>		

</p>
