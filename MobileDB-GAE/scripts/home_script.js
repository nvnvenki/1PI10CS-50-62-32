(function(){
	var units = {
		'Price' : ' EUR',
		'talktime' : ' hrs',
		'camera' : ' MP',
		'os':'',
		'GPS':'',
		'Bluetooth':''

	}
	function display_results(response_data)
	{
			
			if($("body").find("div.results"))
			{
				$("div.results").remove();
			}
			if($("body").find("h2#result-text"))
			{
				$("h2#result-text").remove();
			}

			var response_json = $.parseJSON(response_data)
		
			var result = response_json['result']; // This is the list of json
			// console.log(result)
			var total_results = result.length;
			
			var i = 0;
			$("<h2></h2>",{
				text : "Query Result :" + total_results + " Moblies found",
				id : "result-text"
			}).insertAfter("div.specification");
			if(total_results == 0)
			{
				$("#result-text").addClass('no-mobile')
			}
			else
			{
				$("#result-text").removeClass('no-mobile')
			}
				

			$("<div></div>",{
				class: "results",
			}).insertAfter("#result-text");
			

			$.each(result,function(index,value){
				value = $.parseJSON(value)
				
				$("<h3></h3>",{
					html: "<img src = " + value["image"] + " alt = " + value["brand"] + ">" + "<span id = 'brand-name'>" + value["brand"] + "</span>" ,
					id : i
				}).appendTo(".results");
				
				// For table n smooth transition :)
				$("<div></div>",{
					class: "table_content" + i
				}).insertAfter("h3#" + i);

				// var content = "";
				var table_content = "";
				$.each(value,function(keys){
					
					if(keys !== "brand" & keys !== "image")
					{
						table_content = table_content +  "<tr>" + "<td>" + keys + "</td><td>" + value[keys] + units[keys] +  "</td><tr>" 
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
				
				++i;
				
			});

			$(".results").accordion({
				heightStyle: "content",
				animate : 500,
				collapsible: true,
				icons: { "header": "ui-icon-plus", "activeHeader": "ui-icon-minus" },
				active: false
			}); // set the properties
		
	}


	var check_box_more = ["GPS","Bluetooth","Price"]
	$("div.required-features #less").hide();
	$("div.conditional-features #less").hide();
	$("div.required-features #more").on('click',function(){
		$("div.conditional-features").addClass("conditional-features_clicked")
	
		for(var i = 0; i < check_box_more.length; ++i)
		{
			$("#"+check_box_more[i]).show()
			$("#br" + i).show()
			$("#"+check_box_more[i]+"_label").show()
		}
		$("div.required-features #more").hide();
		$("div.required-features #less").show();
	})

	$("div.required-features #less").on('click',function(){
		for(var i = 0; i < check_box_more.length; ++i)
		{
			$("div.required-features #"+check_box_more[i]).hide()
			$("div.required-features #"+check_box_more[i]+"_label").hide()
			$("div.required-features #br"+i).hide()
		}
		$("div.conditional-features").removeClass("conditional-features_clicked")
		$("div.required-features #more").show();
		$("div.required-features #less").hide();

	})


	var more_condtion_entries = [["GPS","yes or no"],["Bluetooth","yes or no"]]
	$("div.conditional-features #more").on('click', function(){
		for(var i = 0; i < more_condtion_entries.length; ++i)
		{
			$("<label></label>",{
				id:more_condtion_entries[i][0] + "label_c",
				for:more_condtion_entries[i][0]+ "_c",
				text:more_condtion_entries[i][0]
			}).insertBefore("div.conditional-features #more")
			// console.log(more_condtion_entries[i][0])
			$("<input>",{
				type:"text",
				id:more_condtion_entries[i][0] + "_c",
				name:more_condtion_entries[i][0]+ "_c",
				placeholder:more_condtion_entries[i][1]
			}).insertAfter("div.conditional-features #"+more_condtion_entries[i][0] + "label_c")

			$("<br>",{
				id:i + "_c"
			}).insertAfter("div.conditional-features #"+more_condtion_entries[i][0]+ "_c")
			$("div.conditional-features #more").hide()
			$("div.conditional-features #less").show();
		}
	})

	$("div.conditional-features #less").on('click', function(){
		for(var i = 0; i < more_condtion_entries.length; ++i)
		{
			$("div.conditional-features #"+more_condtion_entries[i][0] + "label_c").remove()
			$("div.conditional-features #"+more_condtion_entries[i][0]+ "_c").remove()
			$("div.conditional-features #"+i+"_c").remove()

		}
		$("div.conditional-features #more").show();
		$("div.conditional-features #less").hide();
	})

	
	
	$("#query_form").on('submit',function(e){
		e.preventDefault();
		var requested_features = []
		var requested_conditional_features = []
		var feature_check_boxes = $("div.specification").find("input[type='checkbox']")
		var conditional_features = $("div.specification").find("input[type='text']")
		// console.log(feature_check_boxes)
		// console.log(conditional_features)
		for(var i = 0; i < feature_check_boxes.length; ++i)
		{
			if(feature_check_boxes[i].checked)
			{
				// console.log(feature_check_boxes[i]['id'])
				requested_features.push(feature_check_boxes[i]['id'])
			}
		}
		
		// console.log(requested_features)

		for(var i = 0; i < conditional_features.length; ++i)
		{
			if(conditional_features[i].value)
			{
				// requested_conditional_features.push()
				// console.log(conditional_features[i]['id']+ conditional_features[i].value)
				var id = conditional_features[i]['id']
				var value = conditional_features[i].value
				if(id == "os_c")
				{
					value = "=" + value
				}
				else if(id == "Bluetooth_c" | id == "GPS_c")
				{
					if(value == 'yes')
					{
						value = '=True'
					}
					else
					{
						value = '=False'
					}
				}
				requested_conditional_features.push(id.slice(0,id.length-2) + value)
			}
		}
		// console.log($("#company_selected").val())
		// console.log(requested_conditional_features)
		requested_conditional_features.push("company="+$("#company_selected").val())
		var request_json = {
			"requested_features" : requested_features,
			"conditional_features" : requested_conditional_features
		}

		// console.log(request_json)

		// send the request
		$.post("/query",JSON.stringify(request_json),function(response_data){
			display_results(response_data);
		
		}).done(function(){
			$('html,body').animate({
           		 scrollTop: $("#result-text").offset().top - 15},
            	'slow');

		});
	})
})();