<h1>Mobile Device database engine.</h1>
<p>
This is the Python project , done as a part of python elective course.
<p>
		<h4> Begining stage of the project </h4>
		<hr>
		<h5>commands:(for commandline with inmemory database) </h5>
					<ul>
						<li> save - to load the data to the database </li>
					 <li> query - to query the database</li>
					 <li> close - to close the connection with the server</li>
					</ul>
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
	<p> 
		<h4>Later stages of the project</h4>
		<hr>
		<ul>
			
			<li>The inmemory database is organised according to company names : each company directory contains <br>
				the mobile data of that company - A kind of abstration which makes searching very easier.
			</li>
			<li> As a part of this project a sockect client and socket sever which<br> serves multiple clients are implemented</li>
			<li> A simple web server is written in python which seves multiple <br>clients using rest API(JSON is used here).</li>
			<li> The data is crawled from the website gsmarena.com using regex <br> and later regex is substitudes with beatiful soup libray for crawling </li>
			<li> The database used to store the data is mongodb. In the earlier stages of this project <br>
				an in memory databse is used. </li>
			<li>The project is comepletly ported to google app engine cloud and <br>it uses google data store as database management system</li>
		</ul>
	</p>
	<p> <a href="http://pymobileinfo.appspot.com">Site </a>
		<img src="https://dl.dropboxusercontent.com/u/109288873/pymobile.png"></p></p>
</p>		

</p>
<p>
<h4> contributors: <h4>
  <ul>
    
    <li> Bhuvan (bhuvanlive@gmail.com) </li>
    
    <li> Venkatesh (nvnvenki@gmail.com)</li>
    <li> Pravardhan (pravardhan.kambagi@gmail.com) </li>
  </ul>
</p>
