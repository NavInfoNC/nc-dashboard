import jenkins

def get_status(info):
	return info['color'];

def get_health_report(info):
    for i in info["healthReport"]:
        if i["description"].startswith("Test Result"):
            m = re.match(".*?(\d[,\d]+).*?(\d[,\d]+)", i["description"])
            if m:
                failed = m.group(1).replace(",", "")
                total = m.group(2).replace(",", "")
                return (int(failed), int(total))
    return (0, 0)

server = jenkins.Jenkins('http://build.navicore.mapbar.com', username='robot', password='CheeseSnack')
info = server.get_job_info('NaviCoreAutoTest')

print "query job:", "NaviCoreAutoTest"
print "status:", get_status(info)
print "errors:", get_health_report(info)
