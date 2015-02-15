$(function(){
    $('.comment-form').each(function(){
        var form = $(this);
        form.hide();
        $('<a href="#"> Comment </>').insertAfter(form).click(function(){
            $('.comment-form').hide();
            form.show();
        });
    });
});
