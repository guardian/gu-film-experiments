
jQuery(".star-review-star-btn").on("click", function(event) {
	var $chosenStar = jQuery(event.target);
	var rating = $chosenStar.data("rating");
	var film_id = $chosenStar.parents('.star-review').data('movie-id');
	jQuery(".star-review-stars .star-review-star-btn").removeClass('s-selected');

	

	jQuery.ajax({
		type: "POST",
		dataType: "json",
		url: "http://7.gu-film-experiments.appspot.com/api/star-review",
		data: {
			movie_id: film_id,
			stars: rating
		}
	}).done(function(data) {
		$chosenStar.addClass('s-selected');
		$parentItem = $chosenStar.parents(".star-review-stars-star");
		$parentItem.prevAll().children('.star-review-star-btn').addClass('s-selected');
		jQuery(".star-review-summary ").text(data.ratings_summary_text);	
		jQuery('.star-review-star-btn').removeClass('s-considering').removeClass('s-not-considering');
		jQuery('.star-review-summary-cta').addClass('s-hidden');
		jQuery('.star-review-summary').removeClass('s-hidden');

	}).fail(function() {
		jQuery('.star-review-status').removeClass('s-hidden').show().fadeOut(3000);
	});

});

jQuery(".star-review-star-btn").on("mouseover", function(event) {
	var $chosenStar = jQuery(event.target);
	var rating = $chosenStar.data("rating");

	$chosenStar.addClass('s-considering');
	$parentItem = $chosenStar.parents(".star-review-stars-star");
	$parentItem.prevAll().children('.star-review-star-btn').addClass('s-considering');
	$parentItem.nextAll().children('.star-review-star-btn').addClass('s-not-considering');
});

jQuery(".star-review-star-btn").on("mouseout", function(event) {
	var $chosenStar = jQuery(event.target);
	var rating = $chosenStar.data("rating");

	jQuery('.star-review-star-btn').removeClass('s-considering').removeClass('s-not-considering');
});
		
