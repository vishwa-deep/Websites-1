/**
 * Created by admin on 9/20/2014.
 */
$(function(){
  $('#btnAgain').hide();
  $('#btnReset').hide();
  // capture search results
 	$('.search').on('click', function(e){
 		e.preventDefault();
  	var parameters = { city: $('#city').val()};
  	console.log(parameters)
  	// send results to server
    $.get( '/searching',parameters, function(data) {
    	// handled returned data
    	$('input').hide();
    	$('#btnSearch').hide();
    	$('#btnAgain').show();
    	$('#btnReset').show();
    	$('#results').html(data);
  	});
 	});
 	// reset/start over
 	$('#btnReset').on('click', function(e){
 		e.preventDefault();
 		$('input').val('').show();
    $('#btnSearch').show();
    $('#btnAgain').hide();
    $('#btnReset').hide();
    $('#results').html('');
  });
});