$(document).ready(function() {
	$("table").each(function() {
//		$(this).tablesorter(); 
//		$(this).trigger("sorton",[[1,0]]); 
		$(this).tablesorter({
			sortList : [ [ 1,1 ] ]
		});
//		console.log("bla");
	});
});
