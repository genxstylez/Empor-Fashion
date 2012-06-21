
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
});
