import json
import httplib
new_conn = httplib.HTTPConnection('172.17.42.1:4243')
headers = {"Content-type": "application/json","Accept": "text/plain"}
#image='dc376b561957c5a1b70603f246cde89696042f8b8d1ff7dc768eb1303b316e13'
container = '9a55730ff3c753af4b01c1d3ac254c79a129b14896135300a0f135c8ee6ae136'
#container = '1a8538a4f979'
new_req_body = '{\
"Hostname":"",\
"Domainname": "",\
"User":"",\
"Memory":0,\
"MemorySwap":0,\
"CpuShares": 512,\
"Cpuset": "0,1",\
"AttachStdin":false,\
"AttachStdout":true,\
"AttachStderr":true,\
"PortSpecs":null,\
"Tty":false,\
"OpenStdin":false,\
"StdinOnce":false,\
"Env":null,\
"Cmd":[\
"date"\
],\
"Volumes":{\
"/tmp": {}\
},\
"WorkingDir":"",\
"NetworkDisabled": false,\
"ExposedPorts":{\
"22/tcp": {}\
}\
}'
print new_req_body
#image='76f2fd412141'
#new_req_body = '{"Hostname":"","User":"","Memory":0,"MemorySwap":0,"AttachStdin":true,"AttachStdout":true,"AttachStderr":true,"ExposedPorts":{},"Tty":true,"OpenStdin":true,"StdinOnce":false,"Env":null,"Cmd":["apt-get remove iputils-ping"],"Dns":null,"Image":"'
#new_req_body += str(image)
#new_req_body += '","Volumes":{},"VolumesFrom":"","WorkingDir":"/"}'
#new_conn.request("GET","/images/" + str(image) + "/json")
#new_conn.request("GET", "/containers/create", new_req_body, headers)
msg="yes"
repo="darshan/1"
print container
new_conn.request("POST","/commit?container=" + str(container) + "&comment=" + str(msg) + "&repo=" + str(repo))
r1 = new_conn.getresponse()
print r1.status
print r1.reason
r1=r1.read()
r1=json.loads(r1)
print r1


