var REFRESH_CYCLE = 10000;  // ms

function loadAllData() {

    function getTimeDescription(timestamp) {
        var date = new Date();
        date.setTime(timestamp);

        var now = new Date();
        var yesterday = new Date();
        yesterday.setTime(now.getTime()-1000*60*60*24);
        
        var dayStr;
        if (date.getFullYear() == now.getFullYear() && 
            date.getMonth() == now.getMonth() &&
            date.getDate() == now.getDate())
            dayStr = "Today";
        else if (date.getFullYear() == yesterday.getFullYear() && 
            date.getMonth() == yesterday.getMonth() &&
            date.getDate() == yesterday.getDate())
            dayStr = "Yesterday"
        else
            dayStr = date.getFullYear() + '/' + (date.getMonth()+1) + "/" + date.getDate();

        var minutes = date.getMinutes();
        if (minutes < 10)
            minutes = '0' + minutes;

        return date.getHours() + ":" + minutes + ", " + dayStr;
    }

    function getTimeDescription_interval(timestamp) {
        date = new Date();
        date.setTime(timestamp);
        now = new Date();
        
        interval_ms = now.getTime() - timestamp;
        if (interval_ms <= 1000*60)                           // within a minute
            desc = Math.floor(interval_ms/1000) + " sec";
        else if (interval_ms <= 1000*60*60)                   // within an hour
            desc = Math.floor(interval_ms/1000/60) + " min";
        else if (interval_ms <= 1000*60*60*24)                // within a day
            desc = Math.floor(interval_ms/1000/60/60) + " hr";
        else
            desc = Math.floor(interval_ms/1000/60/60/24) + " day(s)";

        desc += ' ago';
        return desc;
    }

    $.ajaxSettings.async = false;

    document.getElementById('name-1').innerHTML = "NaviCore";
    $.getJSON('/status/NaviCore',
        function (data) {
            document.getElementById('box-1').className = data.status;
            document.getElementById('time-1').innerHTML = getTimeDescription_interval(data.timestamp)
        }
    );
    
    document.getElementById('name-2').innerHTML = "NaviCore Test";
    $.getJSON('/status/NaviCoreAutoTest',
        function (data) {
            document.getElementById('box-2').className = data.status;
            document.getElementById('desc-2').innerHTML = data.failed + " / " + data.total + " tests failed.";
            document.getElementById('time-2').innerHTML = getTimeDescription_interval(data.timestamp)
        }
    );
    $.getJSON('/errors/NaviCoreAutoTest',
        function (data) {
            s = '';
            var cnt = 0, MAX_ITEMS = 8;
            for (var i in data.suites)
                for (var j in data.suites[i].cases)
                    if (data.suites[i].cases[j].status == "FAILED" && cnt < MAX_ITEMS) {
                        s += '<li>' + data.suites[i].cases[j].className + '.' + data.suites[i].cases[j].name + '</li>';
                        cnt++;
                    }
            if (cnt >= MAX_ITEMS)
                s += '<li>......</li>';
            document.getElementById('errors-2').innerHTML = s;
        }
    );
    
    document.getElementById('name-3').innerHTML = "Server";
    $.getJSON('/status/ncservers',
        function (data) {
            document.getElementById('box-3').className = data.status;
            document.getElementById('time-3').innerHTML = getTimeDescription_interval(data.timestamp)
        }
    );
    
    document.getElementById('name-4').innerHTML = "Android";
    $.getJSON('/status/NaviCoreGitAndroid',
        function (data) {
            document.getElementById('box-4').className = data.status;
            document.getElementById('time-4').innerHTML = getTimeDescription_interval(data.timestamp)
        }
    );
    
    document.getElementById('name-5').innerHTML = "iOS";
    $.getJSON('/status/NaviCoreGitMac',
        function (data) {
            document.getElementById('box-5').className = data.status;
            document.getElementById('time-5').innerHTML = getTimeDescription_interval(data.timestamp)
        }
    );
    
    $.ajaxSettings.async = true;
}

window.onload = function() {
    loadAllData();
}

///// Request the status per 1s (async)
//var timer = setInterval(
//    function () {
//        loadAllData();
//    }, REFRESH_CYCLE
//);

/// Request the status per 1s (sync)
var timer = setTimeout(
    function () {
        loadAllData();
        setTimeout(arguments.callee, REFRESH_CYCLE);
    }, REFRESH_CYCLE
);
