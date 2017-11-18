/*function getEvents() {
    $.get("/get_events/6").done(function(data){
        var j = data;
    });
}

$(document).ready(function() {
    $.get("/event_lists1").done(function(data){
        var j = JSON.stringify(data);

        var trial ="";
        for (var i=0; i < data.length; i++) {
            if(i != data.length - 1){
                trial  = trial +
                "{" + "title:" +  data[i]['event_type'] + ", start:" + data[i]['start_date'] + "}" + ",";
            }
            else {
                trial  = trial +
                "{" + "title:" +  data[i]['event_type'] + ", start:" + data[i]['start_date'] + "}";
            }

        }
        console.log(trial);
        var tt = JSON.parse(trial);


        var ee = [
            {
                title: 'My event',
                start: new Date(2017, 10, 16),
                end: new Date(2017, 10, 20)
            },
            {
                title: 'Omo event',
                start: new Date(2017, 10, 18)
            }


        ];

        console.log("ubinj" + typeof (tt));
        console.log((data));
        $('#calendar').fullCalendar({
            editable: true,
            theme: false,
            header: {
                left: 'prev,next today',
                center: 'title',
                right: 'month,listYear'
            },


            displayEventTime: false, // don't show the time column in list view

            // THIS KEY WON'T WORK IN PRODUCTION!!!
            // To make your own Google API key, follow the directions here:
            // http://fullcalendar.io/docs/google_calendar/
            //googleCalendarApiKey: 'AIzaSyDcnW6WejpTOCffshGDDb4neIrXVUA1EAE',

            // US Holidays
            //events: 'en.usa#holiday@group.v.calendar.google.com',


            events: ee,


            // events: [
            //     for(var i=0; i < 3, i++){
            //     {
            //         title: 'My event',
            //         start: new Date(2017, 10, 16)
            //     },
            // }
            // ]
            //events: '/event_lists1',





            eventClick: function(event) {
                // opens events in a popup window
                window.open(event.url, 'gcalevent', 'width=700,height=600');
                return false;
            },

            loading: function(bool) {
                $('#loading').toggle(bool);
            }

        });
    });
});


// $(document).ready(function(){
//
//     $.get("/event_lists1").done(function(data){
//         console.log(data);
//     var events = data;
//
//     var eventsArray = [];
//     console.log('e',events);
//     $.parseJSON(events).forEach(function(element, index){
//          eventsArray.push({
//             band_name:element.band_name,
//             event_type:element.event_type,
//             start_date:new Date(element.start_date).toISOString(),
//             end:new Date(element.end_date).toISOString(),
//
//          })
//       })
//
//     $(function() {
//         $('#calendar').fullCalendar({
//
//             header: {
//                 left: 'prev,next today',
//                 center: 'title',
//                 right: 'month,agendaWeek,agendaDay'
//             },
//             defaultDate: Date.now(),
//             editable: false,
//             eventLimit: true, // allow "more" link when too many events
//             events: eventsArray,
//         });
//     });
//     });
// });*/

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
