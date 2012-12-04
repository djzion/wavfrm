Wavfrm = {
    askToConnect: function() {
        $('#facebook_connect_form').popover({
            title: "Don't loose you stuff!",
            content: 'To access your tracks later, please Connect with Facebook.',
            trigger: 'manual',
            placement: 'left'
        }).popover('show').css('margin-top', '10px')
    }
}

$(function() {

    $('#facebook_connect_form').submit(function() {
        console.log('submit')
        var w = window.open($(this).attr('action'),'facebook_connect','toolbar=0,scrollbars=0,location=0,statusbar=0,menubar=0,width=4600,height=300,left = 312,top = 234');

        return false;
    });

})

/* popup window facebook flow */
function onFacebookConnect() {
    console.log('Facebook connected')
    loggedin = true;
}

if (window.name == 'facebook_connect') {
    window.opener.onFacebookConnect()
    window.close()
}