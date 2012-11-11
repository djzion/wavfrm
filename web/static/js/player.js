function initPlayer() {
    if ($('body').hasClass('framed')) $('.player .content').height($('.player').height() - $('.player .header').height())
    
    $('#jplayer').jPlayer({
        ready: function() {
            console.log('jplayer ready')
            $(this).jPlayer('setMedia', {mp3: tracks[0].fields['url']})  
        },
        swfpath: '/js/',
        supplied: 'mp3',
        cssSelectorAncestor: '.player'
    })

    if (document.location.hash) {
        var query = getQuery()
        if (query.button_color) $('.controls a').css('backgroundColor', '#'+query.button_color)
    }
    
    $(window).resize(function() {
        if ($('body').hasClass('framed')) resizePlayer()   
    })
}

function resizePlayer() {
    $('.player .content').height($('.player').height() - $('.player .header').height()) 
}

function getQuery() {
    var query = window.location.hash.substring(1);
    var queryArray = {}
    var vars = query.split("&");
    for (var i = 0; i < vars.length; i++) {
        var pair = vars[i].split("=");
        queryArray[pair[0]] = pair[1];
    }
    return queryArray;
}