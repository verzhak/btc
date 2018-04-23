
$(window).on("load", address_list_refresh);
$("#address_modal_close").on("click", address_list_refresh);

$("#address_modal").on("show.bs.modal", function(e)
{
	var is_create = ($(e.relatedTarget).data("is_create") == "True");
	var address = "";

	if (is_create)
	{
		var url = $(e.relatedTarget).data("create_url");

		$.ajaxSetup(
		{
			headers: { "X-CSRFToken": getCookie("csrftoken") }
		});
	
		$.ajax(
		{
			url : url,
			type : "POST",
			success : function(json)
			{
				address_refresh(json.address);
			}
		});
	}
	else
	{
		address = $(e.relatedTarget).attr("id");
		address_refresh(address);
	}
});

function address_list_refresh()
{
	var url = $("#address_list").data("address_url");

	$.ajax(
	{
		url : url,
		success : function(data)
		{
			$("#address_list").html(data);
		}
	});
}

function address_refresh(address)
{
	$("#address").text(address);

	$("#address_qrcode").empty();
	$("#address_qrcode").qrcode(
	{
		width : 128,
		height : 128, 
		text: address
	});
}

