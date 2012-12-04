var WavfrmPlayer = (function($) {
    return function() {
        var config

        var defaults = {
            button_color: '52d3d3',
            section_color: '52d3d3'
        }

        var getQuery = function() {
            var query = window.location.hash.substring(1);
            var queryArray = {}
            var vars = query.split("&");
            for (var i = 0; i < vars.length; i++) {
                var pair = vars[i].split("=");
                queryArray[pair[0]] = pair[1];
            }
            return queryArray;
        }

        var init = function($el) {
            var query = getQuery()
            config = $.extend({}, defaults, query)
            if (config.button_color) $('.controls a').css('backgroundColor', '#' + config.button_color)

            $el.jPlayer({
                ready: function() {
                    $(this).jPlayer('setMedia', { mp3: tracks[0].fields['url'] })
                },
                swfpath: '/js/',
                supplied: 'mp3',
                cssSelectorAncestor: '.player'
            })


        }

        return {
            init: init
        }
    }
})(jQuery)