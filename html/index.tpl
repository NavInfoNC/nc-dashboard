<!doctype html>
<html lang="us">

<head>
	<meta charset="utf-8">
	<title>Dashboard</title>
	<link href="/css/jquery-ui.css" rel="stylesheet">
	<link href="/css/type.css" rel="stylesheet">
    <link rel="icon" href="data:;base64,=">
</head>

<body>
	% for item in projects:
        <div id="box-{{item['id']}}">
        </div>
    % end
	<!---->
	<script src="/js/jquery.js"></script>
	<script src="/js/jquery-ui.js"></script>
	<script>
        var projects = new Array();
        $.ajaxSettings.async = false;
        $.get("/getprojects",function(data){
            projects = JSON.parse(data);
        })
        var count = projects.length;
		onload();
		//初始化
		function onload()
        {
            $.get("/getboxinfo",function(data,status){
                var boxInfo = JSON.parse(data);
                //打开dialog
                for (var i=0; i < count; i++)
                {
                    $("#box-"+i).dialog();
                    //$("#box-"+i).parent.addClass("box-type-info");
                }

                //删除无用的class
                $(".ui-widget-content").removeClass("ui-widget-content");
                $(".ui-widget-header").removeClass("ui-widget-header ui-corner-all ui-widget-content");
                $(".ui-widget-header").removeClass("ui-widget-content");
                $(".ui-corner-all").removeClass("ui-corner-all");
                $(".ui-dialog-titlebar-close").remove();

                for (var i=0; i < count; i++)
                {
                    $("#box-"+i).parent().addClass("blue");
                    if (typeof(boxInfo[i]) != "undefined")
                    {
                        $("#box-"+i).parent().css("height",boxInfo[i].height);
                        $("#box-"+i).parent().css("width",boxInfo[i].width);
                        $("#box-"+i).parent().css("top",boxInfo[i].top);
                        $("#box-"+i).parent().css("left",boxInfo[i].left);
                    }
                    $("#box-"+i).html("<div class='text-div' id='name-"+i+"'>\
                        </div><div class='text-div' id='time-"+i+"'></div>\
                        <div class='text-div' id='desc-"+i+"'></div>\
                        <div class='text-div' id='errors-"+i+"'></div>");
                }
            });
		}

		function getBoxInfo(){
            var retjson={};
            for(var i = 0; i < count; i++)
            {
                var key = i + '';
                retjson[key]={
                    height:$("#box-"+i).parent().css("height"),
                    width:$("#box-"+i).parent().css("width"),
                    top:$("#box-"+i).parent().css("top"),
                    left:$("#box-"+i).parent().css("left")
                };
            }
            return JSON.stringify(retjson);
		}
		document.onkeydown = function (e) {
			if (e.key == 'Enter') {
                var passwd = prompt("请输入密码","");
				var info = getBoxInfo();
                $.post("/setboxinfo/"+passwd,info,success=function(msg){
                    alert(msg);
                    window.location.reload();
                });
			}
		}
        $.ajaxSettings.async = true;
        
	</script>
    <script src="/js/index.js">
    </script>
    <script>
        setInterval(updateData,{{refreshInterval}}*1000);
    </script>
</body>

</html>