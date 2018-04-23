
$("#send_modal").on("show.bs.modal", function(e)
{
	var label = $(e.relatedTarget).data("send_label");
	var url = $(e.relatedTarget).data("send_url");
	var success_url = $(e.relatedTarget).data("send_success_url");
				
	$("#send_modal_title").text(label);
	$("#send_form").trigger("reset");
	$("#send_modal").data("send_url", url);
	$("#send_modal").data("send_success_url", success_url);
});

