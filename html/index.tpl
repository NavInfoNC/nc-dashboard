<!doctype html>
<html>
    <head>
        <title>Auto Build Status</title>
        <script type="text/javascript" src="/js/jquery2.2.0.min.js"></script>
        <script type="text/javascript" src="/js/index.js"></script>
        <link rel="stylesheet" type="text/css" href="css/main.css"/>
    </head>

<body>
    <div class="box" style="background-color: black">
      <div id="tile-1">
        <div class="content">
          <p class="project_name" id="name-1"></p>
          <p class="project_desc" id="desc-1"></p>
          <p class="time" id="time-1"></p>
        </div>
      </div>
      % for item in projects:
        <div id="tile-{{item['id']}}">
          <div class="content">
            <p class="project_name" id="name-{{item['id']}}"></p>
            <p class="project_desc" id="desc-{{item['id']}}"></p>
            <p class="time" id="time-{{item['id']}}"></p>
          </div>
        </div>
      % end
    </div>
    
  </body>
</html>
