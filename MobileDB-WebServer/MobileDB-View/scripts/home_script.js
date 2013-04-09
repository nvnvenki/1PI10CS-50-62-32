(function(){
	
	$('form').on('submit',function(event){
		
		if($("body").find("div.results"))
		{
			$("div.results").remove();
		}
		if($("body").find("h2#result-text"))
		{
			$("h2#result-text").remove();
		}
		
		var query_input = $('#query-input').val();
		var json_obj = {
			type : "query",
			query: query_input
		};
		$.post("http://localhost",JSON.stringify(json_obj),function(response_data){
			display_results(response_data);
			
		});
		event.preventDefault();
	});
	$("#logout").on("click",function(){
		window.location.replace("index.html");

	});
	function display_results(response_data)
	{
		var result = eval(response_data["result"]); // This is the list of json
		var total_results = result.length;
		// console.log(total_results)
		var i = 0;
		$("<h2></h2>",{
			text : "Query Result :" + total_results + " Moblies found",
			id : "result-text"
		}).insertAfter(".query-input-field");
		
		$("<div></div>",{
			class: "results",
		}).insertAfter("#result-text");
		
		
		$.each(result,function(index,value){
			$("<h3></h3>",{
				html: "<img src = " + value["Image"] + " alt = " + value["Brand"] + ">" + "<span id = 'brand-name'>" + value["Brand"] + "</span>" ,
				id : i
			}).appendTo(".results");

			// For table n smooth transition :)
			$("<div></div>",{
				class: "table_content" + i
			}).insertAfter("h3#" + i);

			// var content = "";
			var table_content = "";
			$.each(value,function(keys){
				
				if(keys !== "Brand" && keys !== "Image")
				{
					
					// console.log(keys);
					// content = content + keys + " : " + value[keys] + "<br>"; 
					table_content = table_content +  "<tr>" + "<td>" + keys + "</td><td>" + value[keys] + "</td><tr>" 
				}
				
			});

			$("<table></table>",{
				class: "table" + i,
				html: table_content,
				border :"1",
				align: "center",
				cellspacing : "2px",
				width: "auto"
			}).appendTo(".table_content" + i);
			/*
			$("<div></div>",{
					class:"content",
					html : content
			}).insertAfter($("h3#" + i ));
			*/
			++i;
		});
		$(".results").accordion({
			heightStyle: "content",
			animate : 1000,
			collapsible: true,
			icons: { "header": "ui-icon-plus", "activeHeader": "ui-icon-minus" },
			active: false
		}); // set the properties
	}
})();