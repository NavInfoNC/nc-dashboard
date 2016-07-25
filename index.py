#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Build-in modules
import os, re
from bottle import run, static_file, route, template
import urllib
import json

# Third-party module
import jenkins


script_dir = os.path.dirname(os.path.abspath(__file__))
server = jenkins.Jenkins('http://build.navicore.mapbar.com', username='robot', password='CheeseSnack')


def get_status(info):
    status = info['color']
    if status.endswith("_anime"):
        status = status[0:-6] + " building"
    return status


# return (failed_number, total_number)
def get_health_report(info):
    for i in info["healthReport"]:
        if i["description"].startswith("Test Result"):
            m = re.match(".*?(\d[,\d]+).*?(\d[,\d]+)", i["description"])
            if m:
                failed = m.group(1).replace(",", "")
                total = m.group(2).replace(",", "")
                return int(failed), int(total)
    return 0, 0


# return the timestamp of the last build in milliseconds
def get_timestamp(job_name):
    info = eval(urllib.urlopen("http://build.nc.cow/job/" + job_name + "/lastBuild/api/python?pretty=true").read())
    return info["timestamp"]


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


@route('/debug')
def page_debug():
    job_name = 'NaviCoreAutoTest'
    # return server.get_job_info(job_name)
    return server.get_build_info(job_name, 2708)


@route('/status/<job_name>')
def page_status(job_name):
    try:
        info = server.get_job_info(job_name)
        return '{"status": "%s", "timestamp": %d}' % (get_status(info), get_timestamp(job_name))
    except:
        return None


@route('/health/<job_name>')
def page_health(job_name):
    try:
        info = server.get_job_info(job_name)
        failed_num, total_num = get_health_report(info)
        return '{"failed": %d, "total": %d}' % (failed_num, total_num)
    except:
        return None


@route('/errors/<job_name>')
def page_errors(job_name):
    try:
        url = "http://build.nc.cow/job/" + job_name + "/lastCompletedBuild/testReport/api/json?pretty=true"
        return json.loads(urllib.urlopen(url).read())
    except:
        return '{}'
    
run(host='0.0.0.0', port='8009', debug=True)

