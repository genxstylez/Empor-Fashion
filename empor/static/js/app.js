
$(function () {
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
        console.log('sdsdsd');
        var url = $(this).attr('href');
        var target = $(this).parent();
        target.load(url, function() {
            target.toggleClass('itemopen', 150, function() {
            $('#content_wrapper').isotope('reLayout');
            });
        });
    return false;
    });
});
