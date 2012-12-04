Wavfrm = {
    askToConnect: function() {
        $('#facebook_connect_form').popover({
            title: "Don't loose you stuff!",
            content: 'To access your tracks later, please Connect with Facebook.',
            trigger: 'manual',
            placement: 'left'
        }).popover('show')
        var $popover = $('#facebook_connect_form').parents('.nav').find('.popover')
        $popover.css('top', '+=10px')
    },

    getUserInfo: function() {
        var req = $.ajax({
            url: '/api/v1/me/',
            dataType: 'json',
            headers: {'content-type': 'application/json'},
            async: false,
            success: function(data) {
                Wavfrm.user = data.objects[0]
            }
        })
        return Wavfrm.user
    },

    /* popup window facebook flow */
    onFacebookConnect: function() {
        console.log('Facebook connected')
        Wavfrm.getUserInfo()
        loggedin = true;
        $('body').trigger('wavfrm:facebook_connect')
    }

}

$(function() {

    $('#facebook_connect_form').submit(function() {
        console.log('submit')
        var w = window.open($(this).attr('action'),'facebook_connect','toolbar=0,scrollbars=0,location=0,statusbar=0,menubar=0,width=4600,height=300,left = 312,top = 234');

        return false;
    });

})

if (window.name == 'facebook_connect') {
    window.opener.Wavfrm.onFacebookConnect()
    window.close()
}