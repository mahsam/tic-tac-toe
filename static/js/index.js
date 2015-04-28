$(document).ready(function() {

	// render the board
	function renderBoard(data) {
		if (data) {
			$('.cell').html('');
			$('.cell').removeClass('computer').removeClass('human');
			
			// set the board with computer's moves
			for (var i in data.computer_moves)
				$('#'+data.computer_moves[i]).addClass('computer').html('o')

			// set the board with user's moves
			for (var i in data.human_moves)
				$('#'+data.human_moves[i]).addClass('human').html('x')
			
			// show the messages or warnings
			if (data.messages)
				alert(data.messages);
		}
	}

	// create a new game
	$("button").click(function(e) {
		var result = window.confirm('Are you sure you want to start a new game?');
		if (result == false)
			e.preventDefault();

		$.ajax({
			url: "/api/start",
			dataType: "json"
		})
		.done(renderBoard);
	});

	// update the board with new user's choice
	$(".cell").click(function(e) {
		var id = e.target.id
		if (id) {
			$.ajax({
				url: "/api/update",
				method: "POST",
				data: { "cell" : id },
				dataType: "json"
			})
			.done(renderBoard);
		}
	});

	// get the latests state of the board
	$.ajax({
		url: "/api/state",
		dataType: "json"
	})
	.done(renderBoard);
});