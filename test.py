#!/usr/bin/env python

import urllib
import os, re

url = 'http://mapbar:f86f51987e9f910a84f77d5610d6f8e3@build.navicore.cn/job/NaviCoreGitMac/api/json?tree=color,lastBuild[timestamp]'
context = urllib.urlopen(url).read()
print(context)