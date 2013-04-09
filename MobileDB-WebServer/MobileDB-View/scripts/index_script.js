(function(){
	
	//This is an object - a signup form
	var speed = 1000;
	var signupForm = {
		container : $(".signup-container"),
		
		configuration:{
			effect:"fadeToggle"
		},
	
		init: function(){
			$("<span></span>",{
				text: "Click here to signup!",
				id : "signup-text"
			})
				.insertAfter('.signin-button')
				.on('click',this.showForm);
			
			
		},
		
		showForm: function(){
			if ($(".signin-container").find("div.warning-text-invalid-login"))
			{
				$("div.warning-text-invalid-login").remove();
			}
			if(signupForm.container.is(":hidden"))
			{
				signupForm.close.call(signupForm.container);
				signupForm.container[signupForm.configuration.effect](speed);
				$("#signin-form")[0].reset();
				$(".signin-container").fadeOut(speed);

			}

		},

		close: function(){
			var $this = $(this); // signupform container
			if ($this.find('span#close-button').length) return;

			$('<span id = "close-button" data-tooltip = "Close!">X</span>')
				.insertAfter("h3#signup-title")
				.on('click',function(){
				$this[signupForm.configuration.effect](speed);
				$('#signup-form')[0].reset();
				$(".signin-container").fadeIn(speed);
				if ($(".signup-container").find("div.warning-text-invalid-login"))
				{
					$("div.warning-text-invalid-login").remove();
				}
				});
		}
	};

	signupForm.init();

	$('#signin-form').on('submit',function(event){
			var type = "signin";
			var username = $('#username').val();
			var password = $("#password").val();
			var json_obj = {
				username : username,
				password : password,
				type : type
			};
			event.preventDefault();
			$.post("http://localhost",JSON.stringify(json_obj),function(data){
				if(data['status'] == 'True')
				{
					window.location.replace("home.html");
				}
				else
				{
				
					$('#signin-form')[0].reset();
					
						$("<div></div>",{
								html:' Username or password is invalid!',
								class : "warning-text-invalid-login"
							}).appendTo("#signin-here");
			
				}
			});
		});

		$('#signup-form').on('submit',function(event){
			var type = "signup";
			var username = $('#username-s').val();
			var password = $("#password-s").val();
			var email = $('#email').val();
			var name = $('#name').val();
			var json_obj = {
				username: username,
				password: password,
				name: name,
				email: email,
				type: type
			};
			//console.log(JSON.stringify(json_obj));
			event.preventDefault();
			$.post("http://localhost",JSON.stringify(json_obj),function(data){
				//console.log(data);
				if(data['status'] == 'False')
				{
					$("<div></div>",{
						html:' Username already exists!',
						class : "warning-text-invalid-login"
					}).appendTo("#signup-title");
				}
				else
				{
					var toast = new Toast("Signup successful!!");
					toast.makeToast();
					$('#signup-form')[0].reset();
				}
				
			});
		});

		$('#username-s').on("focus",function(event){
			if ($(".signup-container").find("div.warning-text-invalid-login"))
			{
				$("div.warning-text-invalid-login").remove();
			}
		});
		$('#username').on("focus",function(event){
			if ($(".signin-container").find("div.warning-text-invalid-login"))
			{
				$("div.warning-text-invalid-login").remove();
			}
		});
		$('#password').on("focus",function(event){
			if ($(".signin-container").find("div.warning-text-invalid-login"))
			{
				$("div.warning-text-invalid-login").remove();
			}
		});
		
})();