$(document).ready(function(){
    var modal = $('#reviewModal');
    var btn = $('#reviewButton');
    var span = $('.close');

    // Show the modal when the "Write a Review" button is clicked
    btn.click(function() {
        modal.fadeIn();
    });

    // Hide the modal when the "close" span is clicked
    span.click(function() {
        modal.fadeOut();
    });

    // Hide the modal when clicking outside of it
    $(window).click(function(event) {
        if ($(event.target).is(modal)) {
            modal.fadeOut();
        }
    });

    // Handle the form submission with AJAX
    $('#reviewForm').submit(function(event){
        event.preventDefault();
        $.ajax({
            url: '{% url "food_review:add_review_ajax" %}',
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
                'name': $('input[name="name"]').val(),
                'food_type': $('select[name="food_type"]').val(),
                'rating': $('input[name="rating"]').val(),
                'comments': $('textarea[name="comments"]').val()
            },
            success: function(response) {
                modal.fadeOut();
                location.reload(); // Optionally reload the page to update the list of reviews
            },
            error: function() {
                alert('Error adding review.');
            }
        });
    });
});
