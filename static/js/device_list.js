
$(".subscribe").on("click", function(e)
{
	device_toggle(this);
});

$(".unsubscribe").on("click", function(e)
{
	device_toggle(this);
});

function device_toggle(obj)
{
	event.preventDefault();

	var url = $(obj).data("device_toggle_url");

	$.ajax(
	{
		url : url,
        async: false
	});

	device_list_refresh();
}

