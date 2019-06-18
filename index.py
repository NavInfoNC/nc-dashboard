#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Build-in modules
import os, re
from bottle import run, static_file, route, template, request
import urllib
import json
import socket
# 配置文件，读取文件 config.json
Config = ""
rootdir = ""
base_url = ""

def init():
    # Set timeout
    global Config
    global rootdir
    global base_url
    socket.setdefaulttimeout(15)
    rootdir = os.path.dirname(os.path.abspath(__file__))
    base_url = 'http://mapbar:f86f51987e9f910a84f77d5610d6f8e3@build.navicore.cn/job/'
    with open(os.path.join(rootdir,"config.json"),"r") as configStream:
        Config = json.loads(configStream.read())
        configStream.close()

@route('/js/<filepath:path>')
def resource_js(filepath):
    return static_file(filepath, root=os.path.join(rootdir, 'html', 'js'))


@route('/css/<filepath:path>')
def resource_css(filepath):
    return static_file(filepath, root=os.path.join(rootdir, 'html', 'css'))


@route('/fonts/<filepath:path>')
def resource_fonts(filepath):
    return static_file(filepath, root=os.path.join(rootdir, 'html', 'fonts'))

@route('/images/<filepath:path>')
def resource_fonts(filepath):
    return static_file(filepath, root=os.path.join(rootdir, 'html', 'images'))

@route('/')
@route('/index.html')
@route('/index.htm')
@route('/index')
def index():
    return template(open(os.path.join(rootdir, 'html', 'index.tpl')).read(), projects=Config['projects'])


@route('/status/<job_name>')
def page_status(job_name):
    print(job_name)
    try:
        url = base_url + job_name + "/api/json?tree=color,lastBuild[timestamp]"
        info = json.loads(urllib.urlopen(url).read())

        status = info['color']
        if status.endswith("_anime"):
            status = status[0:-6] + " building"

        return '{"status": "%s", "timestamp": %d}' % (status, info['lastBuild']["timestamp"])
    except:
        return '{"status": "timeout", "timestamp": 0}'


@route('/health/<job_name>')
def page_health(job_name):
    result = dict()
    try:
        url = base_url + job_name + "/lastCompletedBuild/testReport/api/json?depth=1&tree=failCount,passCount,skipCount"
        info = json.loads(urllib.urlopen(url).read())

        result['failed'] = info['failCount']
        result['skipped'] = info['skipCount']
        result['total'] = info['failCount'] + info['passCount'] + info['skipCount']

        result_list = list()
        if info['failCount'] > 0:
            url = base_url + job_name + "/lastCompletedBuild/testReport/api/json?depth=1&tree=suites[cases[className,name,status]]"
            info = json.loads(urllib.urlopen(url).read())

            for cases in info['suites']:
                for case in cases['cases']:
                    if case['status'] == 'FAILED' or case['status'] == 'REGRESSION':
                        result_list.append('.'.join([case['className'], case['name']]))
        result['failedList'] = result_list
    except:
        pass
    return result

@route("/setboxinfo/<passwd>",method='POST')
def setboxinfo(passwd):
    data = request.body.readlines()[0]
    if passwd == Config['common']['passwd']:
        with open(os.path.join(rootdir,"data/boxinfo.json"),"w") as stream:
            stream.write(data)
            stream.close()
            return "保存成功"
    return "密码错误"

@route("/getboxinfo")
def getboxinfo():
    if os.path.exists(os.path.join(rootdir,"data/boxinfo.json")) == False:
        with open(os.path.join(rootdir,"data/boxinfo.json"),"w") as stream:
            stream.write("{}")
    
    ret = "{}"
    with open(os.path.join(rootdir,"data/boxinfo.json"),"r") as stream:
        ret = stream.read()
    return ret

@route("/getprojects")
def getprojects():
    return json.dumps(Config['projects'])

if __name__ == '__main__':
    init()
    run(host='0.0.0.0', port='8009', debug=True)

