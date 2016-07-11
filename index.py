#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Build-in modules
import os, re
from bottle import run, static_file, route, template
import urllib

# Third-party module
import jenkins


script_dir = os.path.dirname(os.path.abspath(__file__)) 

colors_to_disp = {'blue': '#3fa7f2', 'yellow': '#f28a3f', 'red': '#d82027'}

server = jenkins.Jenkins('http://build.navicore.mapbar.com', username='robot', password='CheeseSnack')

@route('/rst/<filepath:path>')
def rst(filepath):
    return static_file(filepath, root=os.path.join(os.path.dirname(script_dir), 'raspberry', '_build', 'html'))

@route('/js/<filepath:path>')
def rst(filepath):
    return static_file(filepath, root=os.path.join(script_dir, 'html', 'js'))

@route('/css/<filepath:path>')
def rst(filepath):
    return static_file(filepath, root=os.path.join(script_dir, 'html', 'css'))

@route('/')
@route('/index.html')
@route('/index.htm')
@route('/index')
def index():
    return template(open('index.tpl').read())

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
    
@route('/debug')
def debugInfo():
    jobname = 'NaviCoreAutoTest'
    #return server.get_job_info(jobname)
    return server.get_build_info(jobname, 2708)

@route('/status/NaviCore')
def status_NaviCore():
    info = server.get_job_info('NaviCore')
    return '{"color": "%s"}' % (colors_to_disp[info['color']])
    
@route('/status/NaviCoreAutoTest')
def status_NaviCoreAutoTest():
    info = server.get_job_info('NaviCoreAutoTest')
    failed_num, total_num = get_health_report(info)
    if info is None:
        return '{"color": "#000000", "failed": 0, "total": 0}'
    return '{"color": "%s", "failed": %d, "total": %d}' % (colors_to_disp[info['color']], failed_num, total_num)
    
@route('/errors/NaviCoreAutoTest')
def errors_NaviCoreAutoTest():
    info = eval(urllib.urlopen("http://build.nc.cow/job/NaviCoreAutoTest/lastCompletedBuild/testReport/api/python?pretty=true").read())

    return info
    #s = ""
   # for suite in info['suites']:
    #    for case in suite['cases']:
    #        if case['status'] is 'FAILED':
    #            s += '<li>' + case['className'] + '.' + case['name'] + '</li>'
  #  return s
    
@route('/status/ncservers')
def status_NaviCore():
    info = server.get_job_info('ncservers')
    return '{"color": "%s"}' % (colors_to_disp[info['color']])
    
@route('/status/NaviCoreGitAndroid')
def status_NaviCore():
    info = server.get_job_info('NaviCoreGitAndroid')
    return '{"color": "%s"}' % (colors_to_disp[info['color']])
    
@route('/status/NaviCoreGitMac')
def status_NaviCore():
    info = server.get_job_info('NaviCoreGitMac')
    return '{"color": "%s"}' % (colors_to_disp[info['color']])
    
run(host='0.0.0.0', port='8009', debug=True)

