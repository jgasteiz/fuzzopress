/*
 *	JavaScript code for the sidebar-hider
 *
 */
$(document).ready(function() {
	var SIDEBAR_SHOWN = true;
	$(".toggle-sidebar").click(function() {
		if (SIDEBAR_SHOWN === true) {
			SIDEBAR_SHOWN = false;
			$(".articles").addClass("width-max");
			$(".toggle-sidebar span").html("<<");
			$(".sidebar").removeClass("open");
			$(".sidebar").addClass("close");
			$(".sidebar-content").hide();
		}
		else {
			SIDEBAR_SHOWN = true;
			$(".articles").removeClass("width-max");
			$(".toggle-sidebar span").html(">>");
			$(".sidebar").removeClass("close");
			$(".sidebar").addClass("open");
			$(".sidebar-content").show();
		}
	});
	$(".light-switch").click(function() {
		$("body, nav, aside, .toggle-sidebar, .main-content, footer.main.")
			.toggleClass("night-mode");
	});
});