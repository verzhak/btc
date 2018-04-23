
$("#exchange_modal").on("show.bs.modal", function(e)
{
	var id = $(e.relatedTarget).data("exchange_id");
	var label = $(e.relatedTarget).data("exchange_label");
	var success_url = $(e.relatedTarget).data("exchange_success_url");
	var url = $(e.relatedTarget).data("exchange_url");
				
	$("#exchange_modal_title").text(label);
	$("#exchange_modal").data("exchange_id", id);
	$("#exchange_modal").data("exchange_success_url", success_url);
	$("#exchange_modal").data("exchange_url", url);

	$("#exchange_form").trigger("reset");
	$("#exchange_amount").removeClass("is-invalid");
	$("#exchange_amount_error_message").text("");
});

$("#exchange_submit").on("click", function(event)
{
	event.preventDefault();
	
	var id = $("#exchange_modal").data("exchange_id");
	var amount = $("#exchange_amount").val();
	var success_url = $("#exchange_modal").data("exchange_success_url");
	var url = $("#exchange_modal").data("exchange_url");
	
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
			"id" : id,
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
					case 1:
					{
						message = "Bad value";
						break;
					}
				};

				$("#exchange_amount").addClass("is-invalid");
				$("#exchange_amount_error_message").text(message);
			}
		}
	});
});

