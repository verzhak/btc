
$("#signup_modal").on("show.bs.modal", function(e)
{
	$("#signup_form").trigger("reset");
	$("#signup_login").removeClass("is-invalid");
	$("#signup_email").removeClass("is-invalid");
	$("#signup_password").removeClass("is-invalid");
	$("#signup_error_message").text("");
});

$("#signup_submit").on("click", function(event)
{
	event.preventDefault();
	
	var login = $("#signup_login").val();
	var email = $("#signup_email").val();
	var password = $("#signup_password").val();
	var url = $("#signup_modal").data("signup_url");
	var success_url = $("#signup_modal").data("success_signup_url");

	$.ajaxSetup(
	{
		headers: { "X-CSRFToken": getCookie("csrftoken") }
	});

	$.ajax(
	{
		url : url,
		type : "POST",
		data :
		{
			"login" : login,
			"email" : email,
			"password" : password
		},
		success : function(json)
		{
			if (json.error == null)
				$("#signup_success_modal").modal("show"); 
			else
			{
				var message = "Unknown error";

				switch(json.error)
				{
					case 1:
					{
						message = "Error in registration";
						break;
					}
					case 2:
					{
						message = "One of field is empty";
						break;
					}
				};

				$("#signup_login").addClass("is-invalid");
				$("#signup_email").addClass("is-invalid");
				$("#signup_password").addClass("is-invalid");

				$("#signup_error_message").text(message);
			}
		}
	});
});

$("#signup_success_close").on("click", function(event)
{
	event.preventDefault();
	
	var success_url = $("#signup_success_modal").data("success_signup_url");

	$(location).attr("href", success_url);
});

