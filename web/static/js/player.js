var WavfrmPlayer = (function($) {
    'use strict'

    return function(track_id) {
        var config

        var defaults = {
            button_color: '52d3d3',
            section_color: '52d3d3'
        }

        var init = function($el) {
            var query = WavfrmUtil.getQuery()
            config = $.extend({}, defaults, query)
            if (config.button_color) $('.controls a').css('backgroundColor', '#' + config.button_color)

            $el.jPlayer({
                ready: function() {
                    $(this).jPlayer('setMedia', { mp3: tracks[0].fields['url'] })
                },
                swfpath: '/js/',
                supplied: 'mp3',
                cssSelectorAncestor: '#wavfrm_' + track_id
            })


        }

        return {
            init: init
        }
    }
})(jQuery)