#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Build-in modules
import os, re
from bottle import run, static_file, route, template
import urllib
import json

script_dir = os.path.dirname(os.path.abspath(__file__))

base_url = 'http://mapbar:f86f51987e9f910a84f77d5610d6f8e3@build.nc.cow'

@route('/rst/<filepath:path>')
def rst(filepath):
    return static_file(filepath, root=os.path.join(os.path.dirname(script_dir), 'raspberry', '_build', 'html'))


@route('/js/<filepath:path>')
def resource_js(filepath):
    return static_file(filepath, root=os.path.join(script_dir, 'html', 'js'))


@route('/css/<filepath:path>')
def resource_css(filepath):
    return static_file(filepath, root=os.path.join(script_dir, 'html', 'css'))


@route('/fonts/<filepath:path>')
def resource_fonts(filepath):
    return static_file(filepath, root=os.path.join(script_dir, 'html', 'fonts'))


@route('/')
@route('/index.html')
@route('/index.htm')
@route('/index')
def index():
    return template(open(os.path.join(script_dir, 'html', 'index.tpl')).read())


@route('/status/<job_name>')
def page_status(job_name):
    try:
        url = base_url + "/view/Manual/job/" + job_name + "/api/json?tree=color"
        status = json.loads(urllib.urlopen(url).read())['color']
        if status.endswith("_anime"):
            status = status[0:-6] + " building"

        url = base_url + "/job/" + job_name + "/lastBuild/api/json?tree=timestamp"
        timestamp = json.loads(urllib.urlopen(url).read())["timestamp"]

        return '{"status": "%s", "timestamp": %d}' % (status, timestamp)
    except:
        return None


@route('/health/<job_name>')
def page_health(job_name):
    try:
        url = base_url + "/view/Manual/job/" + job_name + "/api/json?tree=healthReport[description]"

        info = json.loads(urllib.urlopen(url).read())

        failed_num, total_num = 0, 0
        for i in info["healthReport"]:
            if i["description"].startswith("Test Result"):
                m = re.match(".*?(\d[,\d]*).*?(\d[,\d]*)", i["description"])
                if m:
                    failed = m.group(1).replace(",", "")
                    total = m.group(2).replace(",", "")
                    failed_num, total_num = int(failed), int(total)
                    break

        return '{"failed": %d, "total": %d}' % (failed_num, total_num)
    except:
        return None

@route('/errors/<job_name>')
def page_errors(job_name):
    try:
        url = base_url + "/job/" + job_name + "/lastCompletedBuild/testReport/api/json?depth=1&tree=suites[cases[className,name,status]]"
        return json.loads(urllib.urlopen(url).read())
    except:
        return '{}'
    
run(host='0.0.0.0', port='8009', debug=True)

