$(document).ready(function() {

  function ajaxCalls(tellServ) {
    $.ajax({
      url: '/cgi-bin/search.py',
      data: {search: tellServ  },
      dataType: 'json'
    })
    .done(function( data ) {
      var numItems = Object.keys(data).length
      //var numItems = data.keys().length;
      console.log(numItems);
      var colWidth = 12/numItems;

      
      //$.each(json, function(key, val){
      $('#timeline').empty();
      for(var i in data){
        var timespan = i;
        var timeId = data[i].year;
        var photoURL = data[i].image;
        var thumbURL = data[i].thumbnail;
        var archiveURL = data[i].link;
        var photoName = data[i].name;

        console.log(data)
        var largePhoto = '';

        console.log("displaying items");

        if (photoURL !== ''){
          largePhoto = '<a href="#" class="thumbnail sizeable largepic"><img src="'+
          thumbURL +
          '" alt="see larger photo" data-large= "' + photoURL + '" data-caption="' + photoName + '"/></a>'
        }
        else {
          largePhoto = '<span class="thumbnail sizeable"><img src="'+
          thumbURL +
          '" alt="' + photoName + '"/></span>'
        }

        

        $('#timeline').append('<div class="col-md-' +
        colWidth +
        '">' + largePhoto + '<div class="text-center"><p class="original"><a href=""' +
        archiveURL +
        'go to archive</a></p><p class="timeframe"><a class="divein"  id="'+
        timespan +
        '" href="#"></a>'+ timespan +'</p></div></div>' );
      }
    });
  }



  $('#searchform').on('submit', function(){

    var searchQuery = $('#searchquery').val();

    ajaxCalls(searchQuery);

    return false;
  });


  $('.divein').on('click keypress', function(){

       var whichLink = $(this).prop('id');
       console.log("It is being called")
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
