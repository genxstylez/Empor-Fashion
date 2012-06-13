$(function () {

    //menu button binding
    $('div.menu_button a').on('click', function() {
        $('div.menu_pop').fadeIn();
        return false;
    });

    $('div.black_bg').on('click', function() {
        $('div.menu_pop').fadeOut();
    });
});
