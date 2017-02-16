#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Build-in modules
import os, re
from bottle import run, static_file, route, template
import urllib
import json
import socket

import jenkinsapi

script_dir = os.path.dirname(os.path.abspath(__file__))

jenkins_url = 'http://build.nc.cow/'
jenkins_user = 'mapbar'
jenkins_pw = '5?vIctOria'
server = jenkinsapi.jenkins.Jenkins(jenkins_url, username=jenkins_user, password=jenkins_pw)

# Set timeout
socket.setdefaulttimeout(30)

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
        job = server.get_job(job_name)
        status = job._data['color']
        if status.endswith("_anime"):
            status = status[0:-6] + " building"

        lastbuild = jenkinsapi.api.get_latest_build(jenkins_url, job_name, jenkins_user, jenkins_pw)
        timestamp = lastbuild._data['timestamp']

        return '{"status": "%s", "timestamp": %d}' % (status, timestamp)
    except:
        return None


@route('/health/<job_name>')
def page_health(job_name):
    try:
        lastbuild = jenkinsapi.api.get_latest_build(jenkins_url, job_name, jenkins_user, jenkins_pw)
        failed_num = lastbuild._data['actions'][2]['failCount']
        total_num = lastbuild._data['actions'][2]['totalCount']

        return '{"failed": %d, "total": %d}' % (failed_num, total_num)
    except:
        return None


@route('/errors/<job_name>')
def page_errors(job_name):
    try:
        lastbuild = jenkinsapi.api.get_latest_build(jenkins_url, job_name, jenkins_user, jenkins_pw)
        resultset = lastbuild.get_resultset()
        return resultset._data
    except:
        return '{}'
    
run(host='0.0.0.0', port='8009', debug=True)

