$(function() {
    var waveform_id, track_id, pollCount = 0;
    var statusPercentages = {
        waiting: 10,
        downloading: 30,
        processing: 50,
        drawing: 70,
        echonest: 90,
        complete: 100
    }

    var showResult = function() {
        var imgHtml = '<img src="http://' + document.location.host + '/waveform/' + waveform_id + '/img/" />'
        //$('#img_container').html(imgHtml)
        $('#img_tag').val(imgHtml)
        var hashParams = preparePost($('#hashform'))
        var hashQuery = '#' + $.param(hashParams)
        $('#player').attr('src', '/player/' + waveform_id + '/' + hashQuery)

        $('#embed_code').val('<iframe width="100%" height="240px" src="http://' + document.location.host + '/player/' + waveform_id + '/' + hashQuery + '" scrolling="no" border="0"></iframe>')
        $('#result').show()
    }

    var pollStatus = function() {
        $.getJSON('/waveform/' + waveform_id + '/', function(data) {
            $('#status h2').html(data.status)
            if (data.status == 'complete' || data.status == 'error') {
                $('#status h2').html('Complete!')
                $('#status').slideUp().delay(3000)
                showResult()
                return
            }
            $('#status .progress .bar').width(statusPercentages[data.status] + '%')
            pollCount++
            if (pollCount <= 100) setTimeout(pollStatus, 2000)
        })
    }

    var preparePost = function(form) {
        var params = form.serializeArray(true)
        var post = {}
        params = _.filter(params, function(param) { return param.value != '' })
        $(params).each(function(i, param) {
            if (param.value[0] == '#') params[i].value = param.value.replace('#', '')
            post[param.name] = param.value
        })
        return post
    }

    $('#submit').click(function() {
        var form = $('#track_form')
        var post = preparePost(form)
        $.getJSON('/waveform/', post, function(data) {
            if (!loggedin) Wavfrm.askToConnect()
            waveform_id = data.waveform_id
            track_id = data.track_id
            if (data.status == 'complete') {
                showResult()
                return
            }
            $('#status').show()

            pollStatus()
        })
        return false
    })

    $('input.colorpicker').spectrum({
        showInput: true
    });
})