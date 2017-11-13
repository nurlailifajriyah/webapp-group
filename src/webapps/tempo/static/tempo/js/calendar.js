function getEvents() {
    $.get("/event_lists1").done(function(data){
        var j = data;
    });
}

$(document).ready(function() {
    $.get("/event_lists1").done(function(data){
        var j = JSON.stringify(data);
        console.log(typeof (data));
        $('#calendar').fullCalendar({

            header: {
                left: 'prev,next today',
                center: 'title',
                right: 'month,listYear'
            },


            displayEventTime: false, // don't show the time column in list view

            // THIS KEY WON'T WORK IN PRODUCTION!!!
            // To make your own Google API key, follow the directions here:
            // http://fullcalendar.io/docs/google_calendar/
            googleCalendarApiKey: 'AIzaSyDcnW6WejpTOCffshGDDb4neIrXVUA1EAE',

            // US Holidays
            // events: 'en.usa#holiday@group.v.calendar.google.com',
            // events: j,



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

