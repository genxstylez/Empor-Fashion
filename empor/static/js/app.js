function show_content() {
    $('#modal_overlay').fadeIn(200);
    $('#content_pane').fadeIn(200);
}
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
        masonry: {columnWidth: 170}
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
        var that = $(this).parent();
        var url = $(this).attr('href');
        var target = $('#content_pane');
        target.load(url, function() {
            that.hide();
            setTimeout('show_content();', 180);
        });
        $('#content_pane .close').livequery('click', function() {
            $('#content_pane').fadeOut(400);
            $('#modal_overlay').hide();
            that.fadeIn(200);
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
        $('#content_pane').hide();
        var item = $('.product_option.selected a').attr('data');
        if(!item)
            item = $(this).attr('data');
        var qty = $('#quantity').val();
        $.post('/cart/add/', {'product_id': item, 'quantity': qty}, function(response) {
            $('body').append(response).hide().fadeIn();
            $('.cart .close').livequery('click', function() {
                $('.cart').fadeOut(function() {$(this).remove(); $('#modal_overlay').hide();});
            });
            $('.cart #continue').livequery('click', function() {
                $('.cart').fadeOut(function() {$(this).remove(); $('#modal_overlay').hide();});
            });
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
