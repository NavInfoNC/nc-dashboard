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

# return (failed_number, total_number)
def get_health_report(info):
    for i in info["healthReport"]:
        if i["description"].startswith("Test Result"):
            m = re.match(".*?(\d[,\d]+).*?(\d[,\d]+)", i["description"])
            if m:
                failed = m.group(1).replace(",", "")
                total = m.group(2).replace(",", "")
                return (int(failed), int(total))
    return (0, 0)

def get_status(info):
    status = info['color']
    if status.endswith("_anime"):
        status = status[0:-6] + " building"
    return status
    
# return the timestamp of the last build in milliseconds
def get_timestamp(jobname):
    info = eval(urllib.urlopen("http://build.nc.cow/job/" + jobname + "/lastBuild/api/python?pretty=true").read())
    return info["timestamp"]

@route('/debug')
def debugInfo():
    jobname = 'NaviCoreAutoTest'
    #return server.get_job_info(jobname)
    return server.get_build_info(jobname, 2708)

@route('/status/NaviCore')
def status_NaviCore():
    jobname = 'NaviCore'
    info = server.get_job_info(jobname)
    return '{"status": "%s", "timestamp": %d}' % (get_status(info), get_timestamp(jobname))
    
@route('/status/NaviCoreAutoTest')
def status_NaviCoreAutoTest():
    jobname = 'NaviCoreAutoTest'
    info = server.get_job_info(jobname);
    failed_num, total_num = get_health_report(info)
    return '{"status": "%s", "failed": %d, "total": %d, "timestamp": %d}' % (get_status(info), failed_num, total_num, get_timestamp(jobname))
    
@route('/errors/NaviCoreAutoTest')
def errors_NaviCoreAutoTest():
    page = urllib.urlopen("http://build.nc.cow/job/NaviCoreAutoTest/lastCompletedBuild/testReport/api/json?pretty=true").read()
    try:
        jsonVal = json.loads(page)
    except:
        return ''
    else:
        return jsonVal
    
@route('/status/ncservers')
def status_ncservers():
    jobname = 'ncservers'
    info = server.get_job_info(jobname)
    return '{"status": "%s", "timestamp": %d}' % (get_status(info), get_timestamp(jobname))
    
@route('/status/NaviCoreGitAndroid')
def status_NaviCoreGitAndroid():
    jobname = 'NaviCoreGitAndroid'
    info = server.get_job_info(jobname)
    return '{"status": "%s", "timestamp": %d}' % (get_status(info), get_timestamp(jobname))

    
@route('/status/NaviCoreGitMac')
def status_NaviCoreGitMac():
    jobname = 'NaviCoreGitMac'
    info = server.get_job_info(jobname)
    return '{"status": "%s", "timestamp": %d}' % (get_status(info), get_timestamp(jobname))

    
run(host='0.0.0.0', port='8009', debug=True)

