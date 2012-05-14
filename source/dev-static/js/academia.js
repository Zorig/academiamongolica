$(function() {
  $('input#lookup').autocomplete({
    serviceUrl: '/lookup',
    deferRequestBy: 0,
    noCache: false,
    onSelect: function() {
      $('form#search').submit();
    }
  });

  $('.translation').click(function() {
    $('.translation').css('background', '#fff');
    $(this).css('background', '#f0f0f0');

    $('#js-sidebar').hide();
    var translation_id = $(this).attr('data-translation-id');

    $.ajax({
      url: '/ajax_comments',
      type: 'GET',
      data: {'translation_id': translation_id},
      success: function(data) {
        $('#js-comments').html(data).hide().fadeIn();
      }
    });
  });
});


var vote = function(translation_id, val) {
  $.ajax({
    url: '/ajax_vote',
    type: 'POST',
    dataType: 'json',
    data: {
      'translation_id': translation_id,
      'val': val
    },
    success: function(data) {
      if (data.info == 'NOTLOGGEDIN') {
        alert('Та системд нэвтрээгүй байна');
      } else if (data.info == 'DUPLICATE') {
        alert('Та адилхан санал өгсөн байна');
      } else {
        $('#js-vote-count-' + data.translation_id).text(data.vote);
      }
    }
  });
};

var do_comment = function(el) {
  $.ajax({
    url: '/ajax_comments',
    type: 'POST',
    data: {
      'translation_id': $(el).parent().find('input[name="translation_id"]').val(),
      'comment': $(el).parent().find('.js-comment').val()
    },
    success: function(data) {
      $('#js-comments').html(data).hide().fadeIn();
    }
  });

  return false;
};
