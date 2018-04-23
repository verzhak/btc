
$("#signin_modal").on("show.bs.modal", function(e)
{
	$("#signin_form").trigger("reset");
	$("#signin_login").removeClass("is-invalid");
	$("#signin_password").removeClass("is-invalid");
	$("#signin_error_message").text("");
});

$("#signin_submit").on("click", function(event)
{
	event.preventDefault();
	
	var login = $("#signin_login").val();
	var password = $("#signin_password").val();
	var url = $("#signin_modal").data("signin_url");
	var success_url = $("#signin_modal").data("success_signin_url");

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
			"password" : password
		},
		success : function(json)
		{
			if (json.error == null)
			{
				$(location).attr("href", success_url);
			}
			else
			{
				var message = "Unknown error";

				switch(json.error)
				{
					case 0:
					{
						message = "Please sign in";
						break;
					}
					case 1:
					{
						message = "Your account is not activated";
						break;
					}
					case 2:
					{
						message = "Invalid login, please try again";
						break;
					}
				};

				$("#signin_login").addClass("is-invalid");
				$("#signin_password").addClass("is-invalid");

				$("#signin_error_message").text(message);
			}
		}
	});
});

