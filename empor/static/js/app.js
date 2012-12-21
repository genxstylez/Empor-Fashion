function closeBox() {
	$('img.temp').remove();
	$('body').css({'overflow': 'auto', 'margin-right': 0});
	$('#footer').css('margin-right', 0);
    $('#content_pane').children().remove();
    $('#modal_overlay').hide();
    $('.index_itembox:hidden').fadeIn(400);
    a = location.pathname.split('/');
    History.pushState(null, null, a.splice(0, a.length-2).join('/') + '/');
}

$(window).load(function() {
    //paypal form auto submit
    $('form[name="paypal"]').livequery(function() {
        $(this).submit();
    });
});

$(function() {
    window.modal_close = true;

    if (typeof(flashMessage) != 'undefined') {
        $.jGrowl(flashMessage, {
            position: 'bottom-right'
        });
    }
        
    //lazyload
    $('img.lazy').lazyload({
        effect: 'fadeIn'
    });
    
    $('#single').livequery('click', function() {
        $.fancybox($(this));
        return false;
    });

	$("a.gallery").livequery('click', function() {
        items = $('.fancybox-thumb');
        window.a = items;
        start = items.splice($('.fancybox-thumb.active').index(), $(items).length)
        end = items.splice(0, $('.fancybox-thumb.active').index());
        items = $.merge(start, end)
        $.fancybox(items, {
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
        return false;
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
            $('#shipping_twzipcode').twzipcode({
                countyName: 'shipping_county',
                districtName: 'shipping_district',
                zipcodeName: 'shipping_zip',
                zipcodeSel: $('input[name="billing_zip"]').val()
            });
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
        var parent = $(this).parent();
        parent.addClass('active');
        parent.siblings().removeClass('active');
        //if(parent.index() != $('div.small a.fancybox-thumb:first').index())
          //  parent.insertBefore('div.small a.fancybox-thumb:first');
        var src = $(this).attr('src');
        var large_src = $(this).attr('rel');
        var current_img = $('div.large img:first');
        var large_height = parseInt(330 / $(this).attr('medium_width') * $(this).attr('medium_height'));
        image = new Image();
        $(image).attr({'src': large_src, 'rel': src});
        $(image).hide().appendTo('div.large');
        image.onload = function() { $(this).fadeIn(800); }
        //current_img.fadeOut(1200, function() { 
         //   console.log($(this));
           // $(this).remove(); 
        //});
        current_img.remove();
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
            $('body').append(response).hide().fadeIn(400);
        });
        return false;
    });

    $('a.brand_dynamic').livequery('click', function() {
        if (History.enabled) {
			var that = $(this).parent();
            var url = $(this).attr('href');
            var image = new Image();
            var img = $('img', this);
			History.pushState(null, null, url);
            $('#modal_overlay').fadeIn();
			$('body').css({'overflow': 'hidden', 'margin-right': '15px'});
			$('#footer').css('margin-right', '15px');
            $(image).attr({'src': img.attr('src'), 'width': img.width(), 'class': 'temp'});
            $(image).css({'position': 'fixed', 'z-index': '9999', 'top': $(img).offset().top - $(window).scrollTop(), 'left': $(img).offset().left });
            $(image).appendTo('body');
            image.onload = function () {
                $('#modal_overlay').fadeIn();
                that.hide();
                $(image).animate({
                    'left': $(window).width()/ 2 - 427,
                    'top': 50,
                    'height': $(img).attr('real_he'),
                    'width': $(img).attr('real_wid'),
                }, 400, function() {
					$('#content_pane').addClass('itemopen');
                    $('#content_pane').fadeIn(100);
                    $.get(url, function(response) {
                        $(response).find('.itemopen > *').appendTo($('#content_pane'));
						$(image).remove();
                    });
                });
            }
            return false;
        }
    });
    
    $('a.dynamic').livequery('click', function() {
        if (History.enabled) {
            var that = $(this).parent();
            var img = $('.itemimg img', that);
            var url = $(this).attr('href');
            var image = new Image();
            History.pushState(null, null, url);
            $('#modal_overlay').fadeIn();
			$('body').css({'overflow': 'hidden', 'margin-right': '15px'});
			$('#footer').css('margin-right', '15px');
            $(image).attr({'src': img.attr('src'), 'width': img.width(), 'class': 'temp'});
            $(image).css({'position' : 'fixed', 'z-index': '9999', 'top': $(img).offset().top - $(window).scrollTop(), 'left': $(img).offset().left });
            $(image).appendTo('body');
            image.onload = function() {
                var height = parseInt(330 / img.width() * img.height())
				that.hide();
                $(image).animate({
                    'left': $(window).width() / 2 - 407,
                    'top': 71,
                    'height': height,
                    'width': '330px'
                }, 400,  function() {
					$('#content_pane').addClass('itemopen');
                    $('#content_pane').fadeIn(100);
                    $.get(url, function(response) {
						if($('#content_pane').children().length > 0)
							$('#content_pane').children().remove();
                        $(response).find('.itemopen > *').appendTo($('#content_pane'));
						$(image).remove();
                    });
                });
            }
            return false;
        }
    });

	$('#modal_overlay').livequery('click', function() {
        if(modal_close)
		    closeBox();
        else
            modal_close = true;
	});

    $(document).keyup(function(e) {
        if(e.keyCode === 27)
            closeBox();
    });

    $('#content_pane .close').livequery('click', function() {
        closeBox();
        return false;
    });

	$('#content_pane').livequery('click', function() {
        modal_close=false;
	});
    
    $('#content_pane .close_button').livequery('click', function() {
        closeBox();
        return false;
    });

	$('.menu_content .close').livequery('click', function() {
        $('#menuopen_wrapper').fadeOut(400, function() {
            $(this).remove();
        });
	});

	$('.menu_content').livequery('click', function() {
		$('#menuopen_wrapper').fadeOut(400, function() {
            $(this).remove();
        });
	});

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

    //voucher check
    $('#voucher_check').livequery('click', function() {
        var that = $(this);
        $.post('/order/voucher-check/', {'voucher_code': $('input[name="voucher_code"]').val(), 'add': true}, function(response) {
            if(response.success) { 
                $('#voucher_item span').html(response.voucher_name);
                $('#voucher_value').html(response.voucher_value);
                $('#voucher_label').fadeOut(200);
                $('#voucher_input').fadeOut(200, function() {
                    $('#voucher_item').fadeIn(200);
                });
                $('span#gross_total').hide().html('NT$' + response.gross).fadeIn(200);
                $('span#discount_total').hide().html('NT$' + response.discount).fadeIn(200);
                $('span#net_total').hide().html('NT$' + response.net).fadeIn(200);
            } else {
                alert('查無此優惠');
            }
        });
        return false;
    });

    $('#reset_voucher').livequery('click', function() {
        $.get('/order/voucher-reset/', function(response) {
            if(response.success) {
                $('#voucher_item').fadeOut(200, function () {
                    $('#voucher_item span').html('');
                    $('#voucher_value').html('');
                    $('#voucher_label').fadeIn(200);
                    $('#voucher_input').fadeIn(200);
                });
                $('span#gross_total').hide().html('NT$' + response.gross).fadeIn(200);
                $('span#discount_total').hide().html('NT$' + response.discount).fadeIn(200);
                $('span#net_total').hide().html('NT$' + response.net).fadeIn(200);
            }
        return false;
        });
    });

});
