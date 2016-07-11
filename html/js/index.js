function loadAllData() {

    document.getElementById('name-1').innerHTML = "NaviCore";
    $.getJSON('/status/NaviCore',
        function (data) {
            $('color-box-1').className = data.color;
        }
    );
    
    document.getElementById('name-2').innerHTML = "NaviCore Test";
    $.getJSON('/status/NaviCoreAutoTest',
        function (data) {
            $('color-box-2').className = data.color;
            $('desc-2').innerHTML = data.failed + " / " + data.total + " tests failed.";
        }
    );
    $.getJSON('/errors/NaviCoreAutoTest',
        function (data) {
            s = '';
            for (var i in data.suites)
                for (var j in data.suites[i].cases)
                    if (data.suites[i].cases[j].status == "FAILED")
                        s += '<li>' + data.suites[i].cases[j].className + '.' + data.suites[i].cases[j].name + '</li>';
            document.getElementById('errors-2').innerHTML = s;
        }
    );
    
    document.getElementById('name-3').innerHTML = "Server";
    $.getJSON('/status/ncservers',
        function (data) {
            document.getElementById('color-box-3').style.backgroundColor = data.color;
        }
    );
    
    document.getElementById('name-4').innerHTML = "Android";
    $.getJSON('/status/NaviCoreGitAndroid',
        function (data) {
            document.getElementById('color-box-4').style.backgroundColor = data.color;
        }
    );
    
    document.getElementById('name-5').innerHTML = "iOS";
    $.getJSON('/status/NaviCoreGitMac',
        function (data) {
            document.getElementById('color-box-5').style.backgroundColor = data.color;
        }
    );
    
}

window.onload = function() {
    loadAllData();
}

/// Request the status per 1s
var interval = setInterval(
    function () {
        loadAllData();
    }, 10000
);