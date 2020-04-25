$(function() {
    // Menu dropdown
    $('.menu-button').click(function() {
        if (!$('.searchbar').hasClass('show')) {
            $(this).addClass('flip');
            $('.searchbar').addClass('show');
        } else {
            $(this).removeClass('flip');
            $('.searchbar').removeClass('show');
        }
    })
});