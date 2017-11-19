    $(document).ready(function() {
	    var band_id = $('.band_id').attr('id');

		$('#calendar').fullCalendar({
			header: {
				left: 'prev,next today',
				center: 'title',
				right: 'month,basicWeek,basicDay'
			},
			defaultDate: '2017-11-12',
			navLinks: true, // can click day/week names to navigate views
			editable: true,
			eventLimit: true, // allow "more" link when too many events
			events: '/get_events/' + band_id
    }
		);

	});
