$(document).ready(function () {
    var band_id = $('.band_id').attr('id');

    $('#calendar').fullCalendar({
            header: {
                left: 'prev,next today',
                center: 'title',
                right: 'month,basicWeek,basicDay'
            },
            defaultDate: '2017-11-12',
            navLinks: true, // can click day/week names to navigate views
            editable: false,
            eventLimit: true, // allow "more" link when too many events
            events: '/get_events/' + band_id,

            eventClick: function (calEvent, jsEvent, view) {
                jQuery.noConflict();
                //alert('Event: ' + calEvent.title +' '+ calEvent.start.format("YYYY-MM-DD HH🇲🇲ss") + ' '+ calEvent.end.format("YYYY-MM-DD HH🇲🇲ss"));
                $('#event_modal_body').html( 'Title: '+ calEvent.title  +'<br>'
                    + 'Start: '+calEvent.start.format("YYYY-MM-DD HH:mm:ss")  +'<br>'
                    + 'End: '+calEvent.end.format("YYYY-MM-DD HH:mm:ss")  +'<br>'
                    + 'Related Album: '+'<a href=\"/album_detail/'+  calEvent.album_id + '\">'+calEvent.album+'</a><br>'


                );


                $('#event_modal').modal('toggle');

                // change the border color just for fun
                $(this).css('border-color', 'red');

            }


        }
    );


});