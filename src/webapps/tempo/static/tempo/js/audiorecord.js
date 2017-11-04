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

function

$(document).ready(function () {

  populateList();

  window.setInterval(getUpdates, 5000);

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