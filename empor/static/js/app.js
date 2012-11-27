function closeBox() {
    $('#content_pane').fadeOut(100, function() { $(this).children().remove(); });
    $('#modal_overlay').hide();
    $('.index_itembox:hidden').fadeIn(100);
    if(history.length > 1)
        History.back();
    else {
        a = location.pathname.split('/');
        History.pushState(null, null, a.splice(0, a.length-2).join('/'));
    }
}

$(function() {
    if (typeof(flashMessage) != 'undefined') {
        $.jGrowl(flashMessage, {
            position: 'bottom-right'
        });
    }
    //paypal form auto submit
    $('form[name="paypal"]').livequery(function() {
        $(this).submit();
    });
    
    //lazyload
    $('img.lazy').lazyload({
        effect: 'fadeIn'
    });
	
	$("a.gallery").livequery('click', function() {
        var imgs;
        /*$('.fancybox-thumb').each(function() {
            imgs += { href : $(this).data('thumb') },
        });*/

        $.fancybox(
            $('.fancybox-thumb'),
            {
            prevEffect	: 'fade',
            nextEffect	: 'fade',
            helpers	: {
                title	: {
                    type: 'outside'
                },
                thumbs	: {
                    width	: 75,
                    height	: 75,
                    source  : function(current) {
                        return $(current.element).data('thumb');
                    }
                }
            }
        });
    });

    $('a.not').livequery('click', function() {
        return false;
    });

    $('.open_btn').click(function() {
        $('#footer').animate({
            'height': '107px'
        }, 400, function() {
            $('#footer').removeClass('small').addClass('open');
            $('#footer .text').hide().fadeIn(400);
            $('.note.open').hide().fadeIn(400, function() { $(this).removeAttr('style') });
        });
    });
    
    $('#footer').livequery('mouseleave', function() {
        if($('#footer').hasClass('open')) {
            $('#footer').animate({
                'height': '16px'
            }, 400, function() {
                $('#footer').removeClass('open').addClass('small');
                $('#footer .text').hide().fadeIn(400);
                $('.note.small').hide().fadeIn(400, function() { $(this).removeAttr('style') });
            });
        }
    });

    //same as billing checkbox
    $('input[name="copy_address"]').click(function() {
        if($(this).is(':checked')) {
            $('input#id_shipping_phone').val($('input#id_billing_phone').val());
            $('input#id_shipping_recipient').val($('input#id_billing_recipient').val());
            $('input#id_shipping_address').val($('input#id_billing_address').val());
            $('input#id_shipping_post_code').val($('input#id_billing_post_code').val());
            $('select#id_shipping_country').val($('select#id_billing_country').val());
        }
    });
    // ajax setup for csrf
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", $('input[name*="csrfmiddlewaretoken"]').val());
        }
    });

    $(window).scroll(function () {
        if ($(this).scrollTop() > 100) {
            $('#back-top').fadeIn(400);
        } else {
            $('#back-top').fadeOut(400);
        }
    });

    $('#back-top').click(function () {
        $('body,html').animate({
            scrollTop: 0
        }, 600);
        return false;
    });
    
    //isotope for index
    $('#isotope_list').isotope({
        itemSelector: '.index_itembox',
        masonry: {columnWidth: 230}
    });

    // order reciept
    $('input[name="reciept_type"]').livequery('click', function() {
        var input = $(this);
        if(input.val() == 2) {
            $('#id_uni_no').removeAttr('disabled');
            $('#id_company_title').removeAttr('disabled');
        } else {
            $('#id_uni_no').attr('disabled', 'disabled');
            $('#id_company_title').attr('disabled', '');
        }
    });

    //menu button binding
 /*   $('div.menu_button a').on('click', function() {
        $('div.menu_pop').fadeIn();
        return false;
    });
*/
    // image gallery
    $('div.small img').livequery('click', function () {
        var src = $(this).attr('src');
        var large_src = $(this).attr('rel');
        var current_img = $('div.large img');
        var large_height = parseInt(330 / $(this).attr('medium_width') * $(this).attr('medium_height'));
        image = new Image();
        $(image).attr({'src': large_src, 'rel': src});
        $(image).hide().appendTo('div.large');
        image.onload = function() { $(this).fadeIn(800); }
        current_img.fadeOut(1200, function() { $(this).remove(); });
        $('div.large').height(large_height);
    });

    // shipping country
    $('#ship_country').livequery(function() {
        var val = $(this).val();
        $.get('/order/shipping/' + val + '/', function(response) {
            if(response.success)
                $('.ship_cost').html(response.shipping);
        });
    });

    $('div.black_bg').on('click', function() {
        $('div.menu_pop').fadeOut();
    });

    $('a.ajax').livequery('click', function() {
        var url = $(this).attr('href');
        $.get(url, function(response) {
            $('body').append(response);
        });
        return false;
    });

    $('a.brand_dynamic').livequery('click', function() {
        if (History.enabled) {
            var that = $(this).find('.index_itembox');
            var url = $(this).attr('href');
            var image = new Image();
            var img = $('img', this);
            $(image).attr({'src': img.attr('src'), 'width': img.width()});
            $(image).css({'position': 'fixed', 'z-index': '9999', 'top': $(img).offset().top - $(window).scrollTop(), 'left': $(img).offset().left });
            $(image).appendTo('body');
            image.onload = function () {
                $('#modal_overlay').fadeIn();
                that.hide();
                $(image).animate({
                    'left': $(window).width()/ 2 - 420,
                    'top': $(window).height() * 0.08,
                    'height': $(img).attr('real_he'),
                    'width': $(img).attr('real_wid'),
                }, 400, function() {
                    $('#content_pane').addClass('itemup');
                    $('#content_pane').fadeIn(100);
                    $.get(url, function(response) {
                        $(response).find('.itemopen').appendTo($('#content_pane'));
                        $(image).remove();
                    });
                });
            }
            History.pushState(null, null, url);
            return false;
        }
    });
    
    $('a.dynamic').livequery('click', function() {
        if (History.enabled) {
            var that = $(this).find('.index_itembox');
            var img = $('.itemimg img', that);
            var url = $(this).attr('href');
            var image = new Image();
            $(image).attr({'src': img.attr('src'), 'width': img.width()});
            $(image).css({'position' : 'fixed', 'z-index': '9999', 'top': $(img).offset().top - $(window).scrollTop(), 'left': $(img).offset().left });
            $(image).appendTo('body');
            image.onload = function() {
                $('#modal_overlay').fadeIn();
                var height = parseInt(330 / img.width() * img.height())
				that.hide();
                $(image).animate({
                    'left': $(window).width() / 2 - 400,
                    'top': $(window).height() * 0.0355 + 21,
                    'height': height,
                    'width': '330px'
                }, 400,  function() {
                    $('#content_pane').addClass('itemup');
                    $('#content_pane').fadeIn(100);
                    $.get(url, function(response) {
                        $(response).find('.itemopen').appendTo($('#content_pane'));
                        $(image).remove();
                    });
                });
            }
            History.pushState(null, null, url);
            return false;
        }
    });

    $(document).keyup(function(e) {
        if(e.keyCode === 27)
            closeBox();
    });

    $('#modal_overlay').livequery('click', function() {
        closeBox();
    });

    $('#content_pane .close').livequery('click', function() {
        closeBox();
        return false;
    });
    
    $('#content_pane .close_button').livequery('click', function() {
        closeBox();
        return false;
    });
    
    /*$('.index_itembox').on('mouseenter', function() {
		if(!$(this).hasClass('focus_item')) {
			$(this).addClass('focus_item');
			$(this).removeClass('isotope-item');
			$('.index_itembox').not(this).css('opacity', 0.4);
		}
		return false;
    });

    $('.index_itembox').on('mouseleave', function() {
		if($(this).hasClass('focus_item')) {
			$(this).removeClass('focus_item');
			$(this).addClass('isotope-item');
			$('.index_itembox').not(this).css('opacity', 1);
		}
		return false;
    });*/

    // cart link
    // default quantity
    $('#quantity').livequery(function() {
        $(this).val(1);
    });

    // product option select
    $('.size_select li').livequery('click', function() {
        if($(this).hasClass('soldout'))
            return false;
        $(this).addClass('selected');
        $(this).siblings().removeClass('selected');
        var data = $(this).children().attr('data');
        $.post('/products/_check_stock/', {'product_id': data }, function(response) {
            if (response.success)
                $('input[name="quantity"]').attr('max', response.item_count);
            else
                $('.help-inline.error').html('<i class="s_icon-error"></i>'+response.message);
        });
        return false;
    });

    // add to cart
    $('a#add_cart').livequery('click', function() {
        var qty = $('input[name="quantity"]').val();

        /*if($('.size_select').length > 0 && $('.size_select .selected').length == 0) {
            $('.help-inline.error').html('<i class="s_icon-error"></i>' + gettext('Please choose a size'));
            return false;
        }
        if(qty == '') {
            $('.help-inline.error').html('<i class="s_icon-error"></i>' + gettext('Please enter quantity'));
            return false;
        }
        */
        var item = $('.size_select .selected a').attr('data');
        if(!item)
            item = $(this).attr('data');
        $.post('/cart/add/', {'product_id': item, 'quantity': qty}, function(response) {
            if (response.message) {
                $('.help-inline.error').html('<i class="s_icon-error"></i>' + response.message);
            } else {
                $(response).hide().appendTo('body').fadeIn(function() {
                    var badge = $('.cart_box span.badge');
                    if(badge.length > 0) {
                        badge.html($('#items_count').val());
                    } else {
                        $('.cart_box').append('<span class="badge">' + $('#items_count').val() + '</span>');
                    }
                });
                closeBox();
            }
        });
        return false;
    }); 

    $('.cart_s .close').livequery('click', function() {
        $('.cart_s').fadeOut(200, function() { $(this).remove(); $('#modal_overlay').hide(); });
    });

    $('.cart_s #continue').livequery('click', function() {
        $('.cart_s').fadeOut(200, function() { $(this).remove(); $('#modal_overlay').hide(); });
        return false;
    });
    
    //remove from cart
    $('a.remove_btn').livequery('click', function() {
        var item = $(this).closest('tr');
        var price = parseInt($('.item_total', item).text());
        var data = $(this).attr('data');
        $.post('/cart/remove/', {'cart': data}, function(response) {
            if(response.success) {
                var badge = $('.cart_box span.badge');
                if(parseInt(badge.html()) > 1) {
                    badge.html($('#items_count').val());
                } else {
                    badge.remove();
                }
                item.fadeOut(200, function() { 
                    $('#gross_total').text('NT$'+response.gross_total);
                    $('#discount_total').text('NT$'+response.discount_total);
                    $('#net_total').text('NT$'+response.net_total);
                    $(this).remove(); 
                });
            }
        });
    return false;
    });
});
