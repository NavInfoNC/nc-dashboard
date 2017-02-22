#!/usr/bin/env python
#-*- coding: utf-8 -*-


# Build-in modules
import os, re
from bottle import run, static_file, route, template
import urllib
import json

MAX_COUNT = 8
script_dir = os.path.dirname(os.path.abspath(__file__))
base_url = 'http://mapbar:f86f51987e9f910a84f77d5610d6f8e3@build.nc.cow/job/'


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
        url = base_url + job_name + "/api/json?tree=color,lastBuild[timestamp]"
        info = json.loads(urllib.urlopen(url).read())

        status = info['color']
        if status.endswith("_anime"):
            status = status[0:-6] + " building"

        return '{"status": "%s", "timestamp": %d}' % (status, info['lastBuild']["timestamp"])
    except:
        return None


@route('/health/<job_name>')
def page_health(job_name):
    result = dict()
    try:
        url = base_url + job_name + "/lastCompletedBuild/testReport/api/json?depth=1&tree=failCount,passCount,skipCount"
        info = json.loads(urllib.urlopen(url).read())
        total = info['failCount'] + info['passCount'] + info['skipCount']

        result['failed'] = info['failCount']
        result['total'] = total

        if info['failCount'] > 0:
            result_list = list()

            url = base_url + job_name + "/lastCompletedBuild/testReport/api/json?depth=1&tree=suites[cases[className,name,status]]"
            info = json.loads(urllib.urlopen(url).read())

            cnt = 0
            for cases in info['suites']:
                for case in cases['cases']:
                    if case['status'] != 'PASSED' and cnt < MAX_COUNT:
                        result_list.append('.'.join([case['className'], case['name']]))
                        cnt += 1
            result['failedList'] = result_list
    except:
        pass

    return result

if __name__ == '__main__':
    run(host='0.0.0.0', port='8009', debug=True)

