$(function () {
    $('.send-mail').click(function () {
        var pk = $(this).attr('rel');
        $('#modal-mail').modal();
        $('#modal-mail').find('form').attr('action', SEND_CHANGELOG_MAIL_URL.replace('0', pk));
    });

    $('.send-slack').click(function () {
        var pk = $(this).attr('rel');
        $('#modal-slack').modal();
        $('#modal-slack').find('form').attr('action', SEND_CHANGELOG_SLACK_URL.replace('0', pk));
    });

    var $pencil = $('<a>').attr({
        'class': 'glyphicon glyphicon-pencil edit',
        'href': CHANGELOG_UPDATE_URL,
    });
    $('.changelog-box:not(.no-edit) h1').hover(function () {
        var has_edit = $(this).find('.edit').length > 0;
        if (!has_edit) {
            $(this).append(
                $pencil.clone().attr(
                    'href',
                    $pencil.attr('href').replace(
                        '0', $(this).parents('.changelog-box').attr('rel')
                    )
                )
            );
        } else {
            $(this).find('.edit').removeClass('hide');
        }
    });
    $('.changelog-box:not(.no-edit) h1').mouseleave(function () {
        $(this).find('.edit').toggleClass('hide');
    });
});
