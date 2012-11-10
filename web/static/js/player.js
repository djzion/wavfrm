$(function() {
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
    
    $(window).resize(function() {
        if ($('body').hasClass('framed')) resizePlayer()   
    })
})

function resizePlayer() {
    $('.player .content').height($('.player').height() - $('.player .header').height()) 
}