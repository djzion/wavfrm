var CanvasPlayer = (function(track_id) {
    var canvas = document.getElementById('waveform'), track, echonest_analysis;
    //if (!canvas) {
        canvas = $(canvas).attr('width', $('.waveform img').width()).attr('height', 200)[0]
    //    $('.waveform').append(canvas)
    //}
    $canvas = $(canvas)
    var ctx = canvas.getContext('2d'), x = 0, y = 0, prev_x, prev_y, max_amp, amp_scale;
    var section_color = '#8ED6FF'

    var getX = function(seconds) {
        return Math.round(seconds * ($canvas.width() / echonest_analysis.duration))
    }

    var plotSegment = function(i, segment) {
        var prev_x = x
        var prev_y= y
        x = getX(segment.start)
        //console.log(segment.amp * amp_scale)
        var y = ($canvas.height() / 2) * (segment.amp * amp_scale)
        ctx.lineWidth = 1
        //ctx.moveTo(x, $canvas.height() / 2  - y)
        //ctx.lineTo(x, $canvas.height() / 2 + y)
        ctx.fillRect(x, $canvas.height() / 2  - y, 1, y*2)
        //ctx.stroke();
    }

    var plotSection = function(i, section) {
        x = getX(section.start)
        delta_x = getX(section.duration)
        var sectionGadient = ctx.createLinearGradient(x, 0, x+30, 0);
        sectionGadient.addColorStop(0, section_color);
        sectionGadient.addColorStop(1, 'rgba(255, 255, 255, 0)');
        ctx.lineWidth = 1
        ctx.strokeStyle = 'rbg(0, 100, 200)'
        ctx.fillStyle = sectionGadient
        ctx.fillRect(x, 0, delta_x, $canvas.height())

        ctx.lineWidth = 1
        ctx.strokeStyle  = 'rbg(200, 100, 0)'

        ctx.fillRect(x, 0, 3, $canvas.height())
    }

    var plotBar = function(i, section) {
        x = getX(section.start)
        ctx.lineWidth = 1
        ctx.strokeStyle = 'rbg(0, 100, 200)'
        ctx.fillRect(x, 0, 1, $canvas.height())
    }

    var calcAmplitude = function() {
        $(echonest_analysis.segments).each(function(i, segment) {
            echonest_analysis.segments[i].amp = Math.pow(10, segment.loudness_max / 20)
        })
    }

    var maxAmplitude = function() {
        max_amp = _.max(echonest_analysis.segments, function(seg) { return seg.amp }).amp
        amp_scale = 1 / max_amp
        return max_amp
    }

    var debug = function() {
        debugger
    }

    var init = function() {
        $.ajax({
            url: '/track/' + track_id + '/', dataType: 'json',
            async: false,
            success: function(data) {
                track = data[0]
                echonest_analysis = JSON.parse(track.fields.echonest_analysis)
                timeexec(calcAmplitude, 'Calculate amplitudes')
                timeexec(maxAmplitude, 'Find max amplitude')
            }
        })

        if (document.location.hash) {
            query = getQuery()
            if (query.section_color) section_color = query.section_color
        }

        timeexec(function() {
            $(echonest_analysis.sections).each(plotSection)
        }, 'Draw sections')
        timeexec(function() {
            //$(echonest_analysis.beats).each(plotBar)
        }, 'Draw beats')
        timeexec(function() {
            return
            ctx.beginPath();
            ctx.moveTo(prev_x, prev_y);
            ctx.strokeStyle = "rgb(50, 50, 50)";
            $(echonest_analysis.segments).each(plotSegment)
            ctx.stroke()
        }, 'Draw segments')

        //ctx.fill()
        debugger
    }

    return {
        init: init,
        debug: debug
    }
})

timeexec = function(func, msg) {
    var start = new Date().getTime()
    var result = func()
    console.log(msg + ': ' + (( new Date().getTime() - start) / 1000) + 's')
    return result
}