
$(function () {
    // ajax setup for csrf
    $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                // Only send the token to relative URLs i.e. locally.
                xhr.setRequestHeader("X-CSRFToken", $('input[name*="csrfmiddlewaretoken"]').val());
            }
    });

    //isotope for index
    $('#content_wrapper').isotope({
        itemSelector: '.index_itembox',
    });

    //menu button binding
    $('div.menu_button a').on('click', function() {
        $('div.menu_pop').fadeIn();
        return false;
    });

    $('div.black_bg').on('click', function() {
        $('div.menu_pop').fadeOut();
    });

    $('a.dynamic').livequery('click', function() {
        var url = $(this).attr('href');
        var target = $(this).parent();
        target.siblings().removeClass('itemopen');
        target.load(url, function() {
            target.toggleClass('itemopen', 150, function() {
            $('#content_wrapper').isotope('reLayout');
            });
        });
    return false;
    });
    
    // cart link
    // default quantity
    $('#quantity').livequery(function() {
        $(this).val(1);
    });

    // product option select
    $('.product_option').livequery('click', function() {
        $(this).addClass('selected');
        $(this).siblings().removeClass('selected');
    });

    // add to cart
    $('a#add_cart').livequery('click', function() {
        var item = $('.product_option.selected a').attr('data');
        if(!item)
            item = $(this).attr('data');
        var qty = $('#quantity').val();
        $.post('/cart/add/', {'product_id': item, 'quantity': qty}, function(response) {
            console.log(response);
        });
        return false;
    }); 
});
