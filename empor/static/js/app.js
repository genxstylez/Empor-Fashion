function show_content() {
    var height = $('.itemopen').height();
    var center_left = position.left - (($(window).width() - 840)/2);
    var center_top = position.top - (($(window).height() - height + 20)/2);
    $('.itemopen').appendTo(target).show();
    target.animate({
        'left': '-='+center_left, 'top': '-='+center_top,
        'width': '840px', 'height': height + 20 + 'px',
        }, 400, function() {
            target.removeClass().addClass('itemup');
            var target_offset = target.offset()
            target.css('left', target_offset.left / $(window).width() * 100 + '%');
            target.css('top', target_offset.top / $(window).height() * 100 + '%');
        }
    ); 
}
$(function () {
    if (typeof(flashMessage) != 'undefined') {
        $.jGrowl(flashMessage, {
            position: 'bottom-right'
        });
    }
    //paypal form auto submit
    $('form[name="paypal"]').livequery(function() {
        $(this).submit();
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
            $('#back-top').fadeIn();
        } else {
            $('#back-top').fadeOut();
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
        masonry: {columnWidth: 170}
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
        image = new Image();
        $(image).attr({'src': large_src, 'rel': src});
        $(image).hide().appendTo('div.large');
        current_img.fadeOut(1500, function() { $(this).remove(); });
        $(image).fadeIn(800);
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
    
    $('a.dynamic').livequery('click', function() {
        var that = $(this).parent();
        var img = $('.itemimg img', that)
        var url = $(this).attr('href');
        window.target = $('#content_pane');
        window.position = that.offset();

        target.css({
            'left': position.left, 'top': position.top, 
            'position': 'absolute', 'margin-left': 0, 
            'margin-top': 0, 'height': that.height(),
            'width': that.width(),
        });

        target.addClass('index_itembox');
        that.hide();
        target.show();
        $('#modal_overlay').show();

        $.get(url, function(response) {
            $(response).hide().insertAfter(target);
            setTimeout("show_content()", 40);
        });

        $('#content_pane .close').livequery('click', function() {
            $('#content_pane').fadeOut(100, function() { $(this).children().remove(); });
            $('#modal_overlay').hide();
            that.show();
        });
    return false;
    });

    $('#content_pane .close').livequery('click', function() {
        $('#content_pane').fadeOut(100, function() { $(this).children().remove(); });
        $('#modal_overlay').hide();
    });
    
    $('.index_itembox').on('mouseenter', function() {
        $('.hide', this).show();
    });

    $('.index_itembox').on('mouseleave', function() {
        $('.hide', this).hide();
    });

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
        return false;
    });

    // add to cart
    $('a#add_cart').livequery('click', function() {
        if($('.size_select').length > 0 && $('.size_select .selected').length == 0) {
            alert('please choose a size');
            return false;
        }
        $('#content_pane').hide();
        $('#modal_overlay').hide();
        var item = $('.size_select .selected a').attr('data');
        if(!item)
            item = $(this).attr('data');
        var qty = $('#quantity').val();
        $.post('/cart/add/', {'product_id': item, 'quantity': qty}, function(response, textStatus, xhr) {
            if (xhr.status == 200) {
                var badge = $('.cart_box span.badge');
                if(badge.length > 0) {
                    badge.html(parseInt(badge.html())+1);
                } else {
                    $('.cart_box').append('<span class="badge">1</span>');
                }
                $(response).hide().appendTo('body').fadeIn();
                $('.cart_s .close').livequery('click', function() {
                    $('.cart_s').fadeOut(200, function() { $(this).remove(); $('#modal_overlay').hide(); });
                    $('.index_itembox').fadeIn(200);
                });
                $('.cart_s #continue').livequery('click', function() {
                    $('.cart').fadeOut(200, function() { $(this).remove(); $('#modal_overlay').hide(); });
                    $('.index_itembox').fadeIn(200);
                });
                $('#content_pane > *').remove();
            }
        });
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
                if(badge.html() != '1') {
                    badge.html(parseInt(badge.html())-1);
                } else {
                    badge.remove();
                }
                item.fadeOut(200, function() { 
                    $('span#total').text(function(index, text) {
                        $(this).text(parseInt(text)-price);
                    });
                    $(this).remove(); 
                });
            }
        });
    return false;
    });
});

$.Isotope.prototype._getCenteredMasonryColumns = function() {    this.width = this.element.width();
    var parentWidth = this.element.parent().width();
        // i.e. options.masonry && options.masonry.columnWidth    
    var colW = this.options.masonry && this.options.masonry.columnWidth ||                  
        // or use the size of the first item
        this.$filteredAtoms.outerWidth(true) ||                  
            // if there's no items, use size of container                  
        parentWidth;        
    var cols = Math.floor( parentWidth / colW );    
        cols = Math.max( cols, 1 );    // i.e. this.masonry.cols = ....    
        this.masonry.cols = cols;    // i.e. this.masonry.columnWidth = ...    
        this.masonry.columnWidth = colW;  };    

$.Isotope.prototype._masonryReset = function() {    
    // layout-specific props    
    this.masonry = {};    // FIXME shouldn't have to call this again    
    this._getCenteredMasonryColumns();    
    var i = this.masonry.cols;    
    this.masonry.colYs = [];    
    while (i--) {
        this.masonry.colYs.push( 0 );
    }  
};  

$.Isotope.prototype._masonryResizeChanged = function() {
    var prevColCount = this.masonry.cols;    // get updated colCount    
    this._getCenteredMasonryColumns();    
    return ( this.masonry.cols !== prevColCount );  
};    

$.Isotope.prototype._masonryGetContainerSize = function() {
    var unusedCols = 0, 
    i = this.masonry.cols;    // count unused columns    
    while ( --i ) {      
        if ( this.masonry.colYs[i] !== 0 ) {
            break;      
        }      
        unusedCols++;
    }        
    return {          
        height : Math.max.apply( Math, this.masonry.colYs ),    // fit container to columns that have been used;          
        width : (this.masonry.cols - unusedCols) * this.masonry.columnWidth        
    };  
};
