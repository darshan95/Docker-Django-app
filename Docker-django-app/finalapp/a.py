import json
import httplib
new_conn = httplib.HTTPConnection('172.17.42.1:4243')
headers = {"Content-type": "application/json","Accept": "text/plain"}
#image='dc376b561957c5a1b70603f246cde89696042f8b8d1ff7dc768eb1303b316e13'
image='76f2fd412141'
new_req_body = '{"Hostname":"","User":"","Memory":0,"MemorySwap":0,"AttachStdin":true,"AttachStdout":true,"AttachStderr":true,"ExposedPorts":{},"Tty":true,"OpenStdin":true,"StdinOnce":false,"Env":null,"Cmd":["apt-get remove iputils-ping"],"Dns":null,"Image":"'
new_req_body += str(image)
new_req_body += '","Volumes":{},"VolumesFrom":"","WorkingDir":"/"}'
new_conn.request("POST", "/containers/create", new_req_body, headers)
r1 = new_conn.getresponse()
print type(r1.status)
print type(r1.reason)
r1=r1.read()
r1=json.loads(r1)
print r1

container_id = r1['Id']

new_conn = httplib.HTTPConnection('172.17.42.1:4243')
headers = {"Content-type": "application/json","Accept": "text/plain"}

new_conn.request("POST", "/containers/"+r1['Id'] + "/wait", new_req_body, headers)
r1 = new_conn.getresponse()
print r1.status
print r1.reason
r1=r1.read()
#r1=json.loads(r1)
print r1


new_conn = httplib.HTTPConnection('172.17.42.1:4243')
headers = {"Content-type": "application/json","Accept": "text/plain"}

new_conn.request("GET", "/containers/"+ container_id + "/top", new_req_body, headers)
r1 = new_conn.getresponse()
print r1.status
print r1.reason
r1=r1.read()
#r1=json.loads(r1)
print r1





"""
container_id = r1['Id']
#new_conn = httplib.HTTPConnection('172.17.42.1:4243')
headers = {"Content-type": "application/json","Accept": "text/plain"}
new_req_body='{"Binds":["/tmp:/tmp"], "Links":[], "LxcConf":{"lxc.utsname":"docker"},"PortBindings":{ "22/tcp": [{ "HostPort": "11022" }] },"PublishAllPorts":false, "Privileged":false, "Dns": ["8.8.8.8"],"DnsSearch": [""],"VolumesFrom": [],"CapAdd": ["NET_ADMIN"], "CapDrop": ["MKNOD"],"RestartPolicy": { "Name": "", "MaximumRetryCount": 0 },"NetworkMode": "bridge","Devices": []}'
new_conn.request("POST", "/containers/" + container_id + "/start" , new_req_body, headers)
r1 = new_conn.getresponse()
print r1.read()
print r1.status
print r1.reason
#new_conn.request("POST", "/containers/" + container_id + "/start" , new_req_body, headers)

#r1 = new_conn.getresponse().read()
"""
