
$("#send_modal").on("show.bs.modal", function(e)
{
	$("#send_form").trigger("reset");
	$("#send_address").removeClass("is-invalid");
	$("#send_amount").removeClass("is-invalid");
	$("#send_error_message").text("");
});

$("#send_submit").on("click", function(event)
{
	event.preventDefault();
	
	var address = $("#send_address").val();
	var amount = $("#send_amount").val();
	var url = $("#send_modal").data("send_url");
	var success_url = $("#send_modal").data("send_success_url");
	
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
			"address" : address,
			"amount" : amount
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
						message = "Unknown error";
						break;
					}
					case 1:
					{
						message = "Bad address or amount";
						break;
					}
				};

				$("#send_address").addClass("is-invalid");
				$("#send_amount").addClass("is-invalid");

				$("#send_error_message").text(message);
			}
		}
	});
});

