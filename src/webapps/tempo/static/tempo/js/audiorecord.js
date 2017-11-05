function populateList() {
    $.get('/get_track')
      .done(function(data) {
          var list = $('#track-list');
          list.data('max-time', data['max-time']);
          list.html('');
          for (var i = 0; i < data.tracks.length; i++) {
              track = data.tracks[i];
              var new_track = $(track.html);
              new_track.data("id", track.id);
              list.append(new_track);
          }
      });
}

function getUpdates(){
    var list = $('#track-list');
    var max_time = list.data("max-time")
    $.get('/get_track' + max_time)
      .done(function(data) {
          list.data('max-time', data['max-time']);
          for (var i = 0; i < data.tracks.length; i++) {
              var track = data.tracks[i];
              var new_track = $(track.html);
              new_track.data("id", track.id);
              list.prepend(new_track);
          }
      });
}


//Source: https://stackoverflow.com/a/33723330/8717427
function play_audio() {
    var trackid = $(this).attr("id");
    $(".my_audio-" + trackid ).trigger('play');

 }

 function stop_audio(){
    var trackid = $(this).attr("id");
    $(".my_audio-" + trackid ).trigger('pause');
    $(".my_audio-" + trackid ).prop("currentTime",0);
 }

$(document).ready(function () {

  populateList();

 window.setInterval(getUpdates, 5000);

 $("#track-list").on('click', ".play-btn", play_audio);
 $("#track-list").on('click', ".stop-btn", stop_audio);

  // CSRF set-up copied from Django docs
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }
  var csrftoken = getCookie('csrftoken');
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  });
});