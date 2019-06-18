// 添加box的名字
for(var i = 0;i < projects.length; i++)
{
    var v = projects[i];
    var fontSize = get_font_size("box-"+i);
    $("#name-"+i).html("<div style='font-size:"+fontSize+"px;'>"+v['name']+"</div>");
}

// 根据box 宽度计算字体大小
function get_font_size(boxid)
{
    var width =parseInt($("#"+boxid).parent().css("width"));
    return Math.min(60,parseInt(width/10)); 
}

updateData();
function updateData() {
    $.ajaxSettings.async = false;
    for (var i = 0; i < projects.length; i++) {
        var v = projects[i];
        $.getJSON('/status/' + v['name'],
            function (data) {
                $("#box-"+i).parent().addClass(data.status);
                if(data.status == "red") {
                    $.getJSON('/health/'+v['name'],function(data2){
                        $('#desc-'+i).html("");
                        $('#errors-'+i).html("");

                        if (data2.failed > 0 && data2.total > 0)
                            text = data2.failed + " failed / " + data2.skipped + " skipped / " + data2.total + " total";
                        else if (data2.failed == 0)
                            text = "No failures (" + data2.skipped + " / " + data2.total + " skipped)";
                        else
                            text = "";
                        $('#desc-'+i).html(text);

                        var errors = "";
                        if (data2.failedList.length > 0) {
                            errors = "<li>" + data2.failedList.sort(function (a, b) { return Math.random() - 0.5 }).slice(0, 8).join("</li><li>") + "</li>";
                            if (data2.failed > 8) {
                                errors += '<li>......</li>';
                            }
                        }
                        $('#errors-'+i).html(errors);
                    });
                }
                $("#time-"+i).html("<div>"+getTimeDescription(data.timestamp)+"</div>")
            }
        );
    }
    $.ajaxSettings.async = true;
}


// timestamp to text
function getTimeDescription(timestamp) {

    function getTimeDescription_exact(timestamp) {
        date = new Date();
        date.setTime(timestamp);
        return date.getFullYear() + '/' + (date.getMonth() + 1) + '/' + date.getDate() + ' ' + date.getHours() + ':' + (Array(2).join(0) + date.getMinutes()).slice(-2);
    }

    function getTimeDescription_interval(timestamp) {
        date = new Date();
        date.setTime(timestamp);
        now = new Date();

        interval_ms = now.getTime() - timestamp;
        if (interval_ms <= 1000 * 60)                           // within a minute
            desc = Math.floor(interval_ms / 1000) + " sec";
        else if (interval_ms <= 1000 * 60 * 60)                   // within an hour
            desc = Math.floor(interval_ms / 1000 / 60) + " min";
        else if (interval_ms <= 1000 * 60 * 60 * 24)                // within a day
            desc = Math.floor(interval_ms / 1000 / 60 / 60) + " hr";
        else
            desc = Math.floor(interval_ms / 1000 / 60 / 60 / 24) + " day(s)";

        desc += ' ago';
        return desc;
    }

    if (timestamp != 0)
        return getTimeDescription_exact(timestamp) + ' (' + getTimeDescription_interval(timestamp) + ')';
    else
        return 'NETWORK ERROR';
}