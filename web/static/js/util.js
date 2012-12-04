WavfrmUtil = {
    getQuery: function() {
        var query = window.location.hash.substring(1);
        var queryArray = {}
        var vars = query.split("&");
        for (var i = 0; i < vars.length; i++) {
            var pair = vars[i].split("=");
            queryArray[pair[0]] = pair[1];
        }
        return queryArray;
    },

    timeExec: function(func, msg) {
        var start = new Date().getTime()
        var result = func()
        console.log(msg + ': ' + (( new Date().getTime() - start) / 1000) + 's')
        return result
    }
}