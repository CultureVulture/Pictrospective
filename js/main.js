$(function() {

  function ajaxCalls(tellServ) {
    $.ajax({
      url: 'http://localhost:8000/search.py',
      data: {search: tellServ  },
      dataType: 'json'
    })
    .done(function( data ) {

      console.log('done!');
      //data.keys()
      var numItems = Object.keys(data).length;
      console.log(numItems);
      var colWidth = numItems/12;

      $.each(data, function(key, val){
        var timespan = key;
        var timeId = timespan;
        var photoURL = data.image;
        var thumbURL = data.thumbnail;
        var archiveURL = data.link;
        var photoName = data.name;

        var largePhoto = '';

        if (photoURL !== ''){
          largePhoto = '<a href="#" class="thumbnail sizeable largepic"><img src="'+
          thumbURL +
          '" alt="see larger photo" data-large= "' + photoURL + '" data-caption="' + photoName + '"/></a>'
        }
        else {
          largePhoto = '<img src="'+
          thumbURL +
          '" alt="' + photoName + '"/>'
        }

        $('#timeline').empty();

        $('#timeline').append('<div class="col-md-' +
        colWidth +
        '"><div class="text-center"><p class="original"><a href=""' +
        archiveURL +
        'go to archive</a></p><p class="timeframe"><a class="divein"  id="'+
        timeId +
        '" href="#"></a></p></div></div>' );
      });
    });
  }



  $('#searchform').on('submit', function(){

    var searchQuery = $('#searchquery').val();

    ajaxCalls(searchQuery);

    return false;
  });


  $('.divein').on('click keypress', function(){

       var whichLink = $(this).prop('id');

       ajaxCalls(whichLink);

       return false;
  });

  var contentStore;

  $('.largepic').on('click keypress', function(){
    var imgURL = $(this).children('img').prop('data-large');
    var imgCaption = $(this).children('img').prop('data-caption');

      contentStore = $('#timeline div').detach();
      $('#timeline').append('<div class="col-md-12 flexy"><a href="#" class="goback"><img class="thebiggie" src="' + imgURL + '"</a><p class="photocaption">' + imgCaption + '</p></div>');

  });

  $('.goback').on('click keypress', function(){

    $('#timeline').empty().append(contentStore);

  });

});
