var placeholder="<div class='star-reviews-placeholder'></div>";]
var movie_id = guardian.film.id;
jQuery('.user-film-reviews-promo').append(placeholder);
jQuery('head').append('<link rel="stylesheet" href="http://gu-film-experiments.appspot.com/static/css/star-review.css">');
jQuery('.star-reviews-placeholder').load('http://gu-film-experiments.appspot.com/components/star-review/'+movie_id+' .star-review', function(){
	jQuery.getScript( "http://gu-film-experiments.appspot.com/static/js/star-review-behaviour.js"); 
});
