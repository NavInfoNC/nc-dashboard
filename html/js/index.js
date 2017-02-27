var REFRESH_CYCLE = 10000;  // ms

function loadAllData() {

    function getTimeDescription(timestamp) {

        function getTimeDescription_exact(timestamp) {
            date = new Date();
            date.setTime(timestamp);
            return date.getMonth() + '/' + date.getDate() + ' ' + date.getHours() + ':' +  (Array(2).join(0) + date.getMinutes()).slice(-2);
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

        return getTimeDescription_exact(timestamp) + ' (' + getTimeDescription_interval(timestamp) + ')';
    }

    $.ajaxSettings.async = false;

    document.getElementById('name-1').innerHTML = "NaviCore";
    $.getJSON('/status/NaviCore',
        function (data) {
            document.getElementById('box-1').className = data.status;
            document.getElementById('time-1').innerHTML = getTimeDescription(data.timestamp);
        }
    );
    
    document.getElementById('name-2').innerHTML = "NaviCore Test";
    $.getJSON('/status/NaviCoreAutoTest',
        function (data) {
            // check auto test building status
            var data_build;
            $.getJSON('/status/NaviCoreTestBuild', function(data_build) {
                if (data.status.indexOf('red') == 0 && data_build.status.indexOf('red') == 0)
                    data.status = 'deep_red' + data.status.substring(3);
            });
            
            document.getElementById('box-2').className = data.status;
            document.getElementById('time-2').innerHTML = getTimeDescription(data.timestamp);
        }
    );
    $.getJSON('/health/NaviCoreAutoTest',
        function (data) {
            document.getElementById('desc-2').innerHTML = "";
            document.getElementById('errors-2').innerHTML = "";

            if (data.failed > 0 && data.total > 0)
                text = data.failed + " failed / " + data.skipped + " skipped / " + data.total + " total";
            else if (data.failed == 0)
                text = "No failures (" + data.skipped + " / " + data.total + " skipped)";
            else
                text = "";
            document.getElementById('desc-2').innerHTML = text;

            var s = "";
            if (data.failedList.length > 0) {
                s = "<li>" + data.failedList.sort(function (a,b) {return Math.random() - 0.5}).slice(0,8).join("</li><li>") + "</li>";
                if (data.failed > 8)
                    s += '<li>......</li>';
            }
            document.getElementById('errors-2').innerHTML = s;
        }
    );
    
    document.getElementById('name-3').innerHTML = "Server";
    $.getJSON('/status/ncservers',
        function (data) {
            document.getElementById('box-3').className = data.status;
            document.getElementById('time-3').innerHTML = getTimeDescription(data.timestamp);
        }
    );
    
    document.getElementById('name-4').innerHTML = "Android";
    $.getJSON('/status/NaviCoreGitAndroid',
        function (data) {
            document.getElementById('box-4').className = data.status;
            document.getElementById('time-4').innerHTML = getTimeDescription(data.timestamp);
        }
    );
    
    document.getElementById('name-5').innerHTML = "iOS";
    $.getJSON('/status/NaviCoreGitMac',
        function (data) {
            document.getElementById('box-5').className = data.status;
            document.getElementById('time-5').innerHTML = getTimeDescription(data.timestamp);
        }
    );

    document.getElementById('name-6').innerHTML = "Linux";
    $.getJSON('/status/NaviCoreLinux',
        function (data) {
            document.getElementById('box-6').className = data.status;
            document.getElementById('time-6').innerHTML = getTimeDescription(data.timestamp);
        }
    );
    
    $.ajaxSettings.async = true;
}

window.onload = function() {
    loadAllData();
}

///// Request the status periodically (async)
//var timer = setInterval(
//    function () {
//        loadAllData();
//    }, REFRESH_CYCLE
//);

/// Request the status periodically (sync)
var timer = setTimeout(
    function () {
        loadAllData();
        setTimeout(arguments.callee, REFRESH_CYCLE);
    }, REFRESH_CYCLE
);
