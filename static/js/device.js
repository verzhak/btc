
$(window).on("load", device_list_refresh);

$(document).ready(function()
{
	$("#device_nav").addClass("active");
});

function device_list_refresh()
{
	var url = $("#device_list").data("device_url");

	$.ajax(
	{
		url : url,
		success : function(data)
		{
			$("#device_list").html(data);
		}
	});
}

