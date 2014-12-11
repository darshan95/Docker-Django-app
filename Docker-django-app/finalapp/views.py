from django.shortcuts import render

# Create your views here.
import socket
import httplib
import json
import os
from docker import Client
from django.core.mail import send_mail
from django.core import serializers
from django.utils.timezone import now as utcnow
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
import datetime
from datetime import datetime as dt
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from finalapp.models import User, Image, Container, User_Image, pushed_images
#from blood.models import Choice, Question, Donor, Recepient, Hospital, Camp, Link, Post, Story,Notification, User
from django.contrib.auth.decorators import login_required

#cli = Client(base_url='unix://var/run/docker.sock',version='1.12')
#emailit="bloodconnect14@gmail.com"


@login_required
def index(request):
    context={}
    return render(request, 'finalapp/index.html',context)

@login_required
def home(request):
    context={}
    return render(request,'finalapp/home.html',context)

@login_required
def deploy_war_app(request,ip_app):
    if request.user.is_authenticated:
        user=request.user.username
    if request.method == 'POST':
        admin=request.POST['admin_pass']
        port_name=request.POST['port_cont']
        url_fin='docker run -d -p '
        url_fin=url_fin+str(port_name)+':'+str(port_name)+" -e TOMCAT_PASS="+str(admin)+" tutum/tomcat"
        os.system(url_fin)
        ip_app=([(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]) 
        ip_app+=':'+str(port_name)
        return HttpResponseRedirect('/finalapp/deploy_war_app/'+(ip_app)+'/')
    uuid=request.user.id
    context={'user':user, 'ip_app':ip_app}
    return render(request,'finalapp/deploy_war_app.html',context)

@login_required
def view_your_images(request):
    if request.user.is_authenticated:
        user=request.user.username
    uuid=request.user.id
    image_list=User_Image.objects.all().filter(uid=uuid)
    '''image_id=[]
    for images in image_list:
        image_id.append(images.id_images)'''
    context={'user':user, 'all_images':image_list}
    return render(request,'finalapp/view_your_images.html',context)


@login_required
def view_your_containers(request):
    if request.user.is_authenticated:
        user=request.user.username
    uuid=request.user.id
    image_list=User_Image.objects.all().filter(uid=uuid)
    image_id=[]
    for images in image_list:
        image_id.append(images.id_images)
    context={'user':user, 'image_id':image_id}
    return render(request,'finalapp/view_your_containers.html',context)



@login_required
def view_all_images(request):
#   os.system('sudo su')
        conn=httplib.HTTPConnection("localhost:4243")
        conn.request("GET","/images/json")
        r1=conn.getresponse()
        r1=json.loads(r1.read())
        '''
        key=r1[0].keys()
        new_key=[]
        for i in key:
            new_key.append(str(i))'''
	r2=Image.objects.all()
        context={'all_images':r2}
        return render(request,'finalapp/view_all_images.html',context)

#   cli = Client(base_url='unix://var/run/docker.sock',version='1.12')
#   allimages=cli.images()
#   print allimages
#   context={}
#   return render(request,'finalapp/view_all_images.html',context)



@login_required
def ask_images(request):
    if request.user.is_authenticated:
        user=request.user.username
    if request.method == 'POST':
        name= request.POST['name']
        return HttpResponseRedirect('/finalapp/pull_images/'+(name)+'/')
    context={'user':user}
    return render(request,'finalapp/ask_images.html',context)


@login_required
def pull_images(request,name):
    conn=httplib.HTTPConnection("localhost:4243")
    image_pull='/images/create?fromImage='
    if name[-1]=="/":
        name=name[:-1]
    print "naaaaaaaaaaaaam"
    print name
    image_pull+=str(name)
    print image_pull
    conn.request("POST",image_pull)
    r1=conn.getresponse()
    a=r1.read()
    r1=a
    #key=r1[0].keys()
    #new_key=[]
    flag=0
    if 'error' not in r1:
        flag=0
        r1=r1.split('\n')[0]
        print r1
        #if "" in r1:
        print "hie hie"
        form = Image()
        form.uid=request.user.id
        #parse_json=json.loads(check)
        r1=json.loads(r1)
        print "asdaaaaaas"
        print r1
        #im_id=r1['id']
        conn=httplib.HTTPConnection("localhost:4243")
        conn.request("GET","/images/" + str(name) + "/json")
        r1=conn.getresponse()
        a=r1.read()
        a=json.loads(a)
        form.id_images = a['Id']
        form.name = name
        #form.id_images = new_img['Id']
        form.os = a['Os']
        form.virtual_size = a['VirtualSize']
        form.created = a['Created']
        print a
        #form.virtual_size = r1['VirtualSize']
        #form.repotags = r1['RepoTags'][0]
        form.save()
    else:
        flag=2
    context={'name':name, 'flag':flag, 'a':a}
    return render(request,'finalapp/pull_images.html',context)


@login_required
def ask_create_container(request):
    if request.user.is_authenticated:
        user=request.user.username
    uuid=request.user.id
    image_list=Image.objects.all().filter(uid=uuid)
    print image_list
    image_id=[]
    for images in image_list:
        image_id.append(images.id_images)

 
 
    if request.method == 'POST':
        image= request.POST['image']
        cmd = request.POST['cmd']
        cmd_list = cmd.split()
        cmd=''
        cmd += cmd_list[0]
        for i in range(1,len(cmd_list)):
            cmd += "\s"
            cmd += cmd_list[i]
        cmd = cmd.replace("/",".")
        return HttpResponseRedirect('/finalapp/create_container/'+(image)+'/' + (cmd) + '/' + 'garb' + '/')

    context={'user':user,'image_id':image_id}
    return render(request,'finalapp/ask_create_container.html',context)





    
@login_required
def create_container(request,image,cmd,cont_id):
    if request.method=="POST":
        print "assfsfasasfads"
        msg = request.POST["msg"]
        repo = request.POST["repo"]
        print msg
        print repo
        if "/" in repo:
            repo = repo.replace("/",".")
        return HttpResponseRedirect('/finalapp/commit_container/'+str(cont_id)+'/' + str(msg) + "/" + str(repo) + "/")
    new_conn = httplib.HTTPConnection('172.17.42.1:4243')
    headers = {"Content-type": "application/json","Accept": "text/plain"}
    print "asddddd"
    print image
    print cmd
    cmd_list = cmd.split("\s")
    print cmd_list
    cmd = ' '.join(cmd_list)
    print cmd
    cmd = cmd.replace(".","/")
    new_req_body = '{"Hostname":"","User":"","Memory":0,"MemorySwap":0,"AttachStdin":false,"AttachStdout":true,"AttachStderr":true,"ExposedPorts":{},"Tty":false,"OpenStdin":false,"StdinOnce":false,"Env":null,"Cmd":["'
    new_req_body += str(cmd)
    new_req_body += '"],"Dns":null,"Image":"'
    new_req_body += str(image)
    new_req_body += '","Volumes":{},"VolumesFrom":"","WorkingDir":""}'
    print new_req_body
    new_conn.request("POST", "/containers/create", new_req_body, headers)
    r1 = new_conn.getresponse()
    ret_dict = r1.read()
    ret_dict = json.loads(ret_dict)
    if r1.status==201 and r1.reason=='Created':
        form=Container()
        form.uid=request.user.id
        form.name_image=image
        form.id_container=ret_dict['Id']
        form.save()
        container_id = ret_dict['Id']
        #print r1['Id'] 
    else:
        container_id = '0'
    
    #print r1.status
    #conn=httplib.HTTPConnection("localhost:4243")    
    #conn.request("POST", "/containers/create",request_body)
    #r1=conn.getresponse()
    #create_container='/images/create?fromImage='
    #print r1.status
    cmd=cmd.split()
    cmd = '\s'.join(cmd)
    bbc = "/finalapp/create_container/" + image + "/" + cmd + "/" + container_id + "/"
    print bbc
    context={'name':ret_dict,'container_id':container_id,'bbc':bbc}
    return render(request,'finalapp/create_container.html',context)

@login_required
def commit_container(request,container_id,msg,repo):
    new_conn = httplib.HTTPConnection('172.17.42.1:4243')
    headers = {"Content-type": "application/json","Accept": "text/plain"}
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
    '''print "container_id"
    print container_id
    print repo
    print msg'''
    repo = repo.replace(".","/")
    if repo[-1] in "/":
        repo = repo[:-1]
    print "reeeeeepo"
    print repo
    new_conn.request("POST","/commit?container=" + str(container_id) + "&comment=" + str(msg) + "&repo=" + str(repo))
    r1 = new_conn.getresponse()
    print r1.status
    print r1.reason
    r2=r1.read()
    r2=json.loads(r2)
    print r2
    if r1.status==201 and r1.reason=="Created":
        new_img_id = r2['Id']
        form = User_Image()
        form.uid=request.user.id
        conn=httplib.HTTPConnection("localhost:4243")
        conn.request("GET","/images/" + str(new_img_id) + "/json")
        r1=conn.getresponse()
        new_img=r1.read()
        new_img=json.loads(new_img)
        print "asdddddddddd"
        print new_img['Id']
        form.id_images = new_img['Id']
        if '/' in repo[-1]:
            repo = repo[:-1]
            #repo = repo.replace("/",".")
        print "reeeeeeeeeeeepo"
        print repo
        form.name = repo
        form.virtual_size = new_img['VirtualSize']
        form.created = new_img['Created']
        form.os = new_img['Os']
        form.cmd = new_img['ContainerConfig']['Cmd']
        form.image = new_img['ContainerConfig']['Image']
        #form.virtual_size = r1['VirtualSize']
        #form.repotags = r1['RepoTags'][0]
        form.save()

        form = Image()
        form.uid=request.user.id
        form.name = repo
        form.virtual_size = new_img['VirtualSize']
        form.id_images = new_img['Id']
        form.created = new_img['Created']
        form.os = new_img['Os']
        form.cmd = new_img['ContainerConfig']['Cmd']
        form.image = new_img['ContainerConfig']['Image']
        #form.virtual_size = r1['VirtualSize']
        #form.repotags = r1['RepoTags'][0]
        form.save()
    else:
        new_img_id = '0'
        new_img={}
    print "new_img"
    print new_img
    context={ 'new_img_id':new_img_id, 'new_img':new_img, 'repo':repo }
    return render(request,'finalapp/commit_container.html',context)


@login_required
def view_all_containers(request):
#   os.system('sudo su')
        conn=httplib.HTTPConnection("localhost:4243")
        conn.request("GET","/containers/json")
        r1=conn.getresponse()
        print r1.status
        a=r1.read()
        a=json.loads(a)
        print a
        context={'all_containers':a}
        return render(request,'finalapp/view_all_containers.html',context)
        
@login_required
def ask_search_images(request):
    if request.user.is_authenticated:
        user=request.user.username
    if request.method == 'POST':
        name = request.POST['search_name']
        print "asdasd"
        return HttpResponseRedirect('/finalapp/search_images/'+(name)+'/')
    context={'user':user}
    return render(request,'finalapp/ask_search_images.html',context)

@login_required
def search_images(request,search_name):
    conn=httplib.HTTPConnection("localhost:4243")
    image_search='/images/search?term='
    image_search+=str(search_name)
    conn.request("GET",image_search)
    r1=conn.getresponse()
    value=json.loads(r1.read())
    print value
    context={'search_name':search_name, 'value':value}
    return  render(request, 'finalapp/search_images.html',context)

@login_required
def ask_del_images(request):
    if request.user.is_authenticated:
        user=request.user.username
    if request.method == 'POST':
        idd= request.POST['id']
        print "asdasd"
        return HttpResponseRedirect('/finalapp/delete_images/'+(idd)+'/')
    uuid=request.user.id
    image_list=Image.objects.all().filter(uid=uuid)
    image_id=[]
    for images in image_list:
        image_id.append(images.id_images)
    context={'user':user, 'image_id':image_id}
    return render(request,'finalapp/ask_del_images.html',context)

@login_required
def ask_del_commited_images(request):
    if request.user.is_authenticated:
        user=request.user.username
    if request.method == 'POST':
        idd= request.POST['id']
        return HttpResponseRedirect('/finalapp/delete_commited_images/'+(idd)+'/')
    uuid=request.user.id
    image_list=User_Image.objects.all().filter(uid=uuid)
    image_id=[]
    for images in image_list:
        image_id.append(images.id_images)
    context={'user':user, 'image_id':image_id}
    return render(request,'finalapp/ask_del_images.html',context)

@login_required
def delete_commited_images(request,idd):
    conn=httplib.HTTPConnection("localhost:4243")
    image_del='/images/'
    image_del+=str(idd)
    print image_del
    conn.request("DELETE",image_del)
    r2=conn.getresponse()
    print r2.status
    r2=r2.read()
    print r2
    if "error" not in r2:
        print idd
        User_Image.objects.filter(id_images=idd).delete()
    #print r1.read()
    #r1=r1.read()
    context={'idd':idd}
    return render(request, 'finalapp/delete_commited_images.html', context)

@login_required
def ask_push_images1(request):
    if request.method=="POST":
        request.session['abc'] = request.POST['username']
        request.session['psw'] = request.POST['password']
        request.session['eail'] = request.POST['email']
        print request.session['abc']
        print request.session['psw']
        print request.session['eail']
        return HttpResponseRedirect('/finalapp/ask_push_images2/')
    return render(request,'finalapp/ask_push_images1.html')

@login_required
def ask_push_images2(request):
    status = os.system('docker login --email=' + request.session['eail'] + ' --password=' + request.session['psw']   + ' --username=' + request.session['abc']) 
    print "asdadsa"
    print status
    if status == 0:
        return HttpResponseRedirect('/finalapp/ask_push_images3/')
    else:
        return HttpResponseRedirect('/finalapp/ask_push_images1/')
    return render(request,'finalapp/ask_push_images2.html')

@login_required
def ask_push_images3(request):
    if request.method=="POST":
        img_name = request.POST['name']
        print "img_name"
        print img_name
        return HttpResponseRedirect('/finalapp/push_images/' + str(img_name) + "/")
    uuid=request.user.id
    image_list=User_Image.objects.all().filter(uid=uuid)
    image_name=[]
    for images in image_list:
        image_name.append(images.name)
    print image_name
    #print image_name[0]
    #image_id=[]
    #for images in image_list:
     #   image_id.append(images.name)
    context={'image_name':image_name}
    print context['image_name']
    return render(request,'finalapp/ask_push_images3.html',context)

@login_required
def push_images(request,img_name):
    print "img_nameaaaaaaaa"
    print img_name
    #if '/' in img_name:
     #   img_name = img_name.replace("/",'')
    #a = request.session['abc']
    c = img_name
    print "saaaaaaaaaaaa"
    print c
    ret = os.system("docker push " + c)
    context = {'ret':ret}
    print ret
    return render(request,'finalapp/push_images.html',context)





@login_required
def delete_images(request,idd):
    conn=httplib.HTTPConnection("localhost:4243")
    image_del='/images/'
    image_del+=str(idd)
    print image_del
    conn.request("DELETE",image_del)
    r2=conn.getresponse()
    print r2.status
    r2=r2.read()
    print r2
    nameit=Image.objects.filter(id_images=idd)
    if(nameit):
        nameit=nameit[0]
        nameit=nameit.name
    else:
        nameit="ubuntu"

    check=Image.objects.filter(id_images=idd)
    if(check):
        check.delete()

    check=User_Image.objects.filter(id_images=idd)
    if(check):
        check.delete()
        
    #print r1.read()
    #r1=r1.read()
    context={'idd':idd, 'nameit':nameit}
    return render(request, 'finalapp/delete_images.html', context)

@login_required
def ask_stop_container(request):

    if request.user.is_authenticated:
        user=request.user.username
    if request.method == 'POST':
        container_id = request.POST['container_id']
        return HttpResponseRedirect('/finalapp/stop_container/'+(container_id)+'/')

    conn=httplib.HTTPConnection("localhost:4243")
    conn.request("GET","/containers/json?all=1")
    r1=conn.getresponse()
    print r1.status
    a=r1.read()
    a=json.loads(a)
    
    image_id=[]
    for image in a:
        image_id.append(image['Id'])
    print image_id
    context={'all_containers':image_id}
    return render(request,'finalapp/ask_stop_container.html',context)


    '''conn=httplib.HTTPConnection("localhost:4243")
    image_del='/containers/json?all=1'
    print image_del
    conn.request("GET",image_del)
    r2=conn.getresponse()
    print r2.status
    r2=json.loads(r2.read())
    image_id=[]
    for image in r2:
        image_id.append(image['Id'])
    context={'user':user,'image_id':image_id}
    return render(request,'finalapp/ask_stop_container.html',context)'''
 
 
 
@login_required
def stop_container(request,container_id):
    new_conn = httplib.HTTPConnection('172.17.42.1:4243')
    headers = {"Content-type": "application/json","Accept": "text/plain"}
    print container_id
    new_req_body='{"Binds":["/tmp:/tmp"], "Links":["redis3:redis"], "LxcConf":{"lxc.utsname":"docker"},"PortBindings":{ "22/tcp": [{ "HostPort": "11022" }] },"PublishAllPorts":false, "Privileged":false, "Dns": ["8.8.8.8"],"DnsSearch": [""],"VolumesFrom": ["parent", "other:ro"], "CapAdd": ["NET_ADMIN"], "CapDrop": ["MKNOD"],"RestartPolicy": { "Name": "", "MaximumRetryCount": 0 },"NetworkMode": "bridge","Devices": []}'
    new_conn.request("POST", "/containers/" + container_id + "/stop" , new_req_body, headers)
    r1 = new_conn.getresponse().read()
    print r1
    context={'name':r1,'name':container_id}
    return render(request,'finalapp/stop_container.html',context)

@login_required
def ask_start_container(request):
    if request.user.is_authenticated:
        user=request.user.username
    if request.method == 'POST':
        container_id = request.POST['container_id']
        return HttpResponseRedirect('/finalapp/start_container/'+(container_id)+'/')
    conn=httplib.HTTPConnection("localhost:4243")
    image_del='/containers/json?all=1'
    print image_del
    conn.request("GET",image_del)
    r2=conn.getresponse()
    print r2.status
    r2=json.loads(r2.read())
    image_id=[]
    for image in r2:
        image_id.append(image['Id'])
    context={'user':user,'image_id':image_id}
    return render(request,'finalapp/ask_start_container.html',context)
 
 
@login_required
def start_container(request,container_id):
    container_id=container_id
    new_conn = httplib.HTTPConnection('172.17.42.1:4243')
    headers = {"Content-type": "application/json","Accept": "text/plain"}
    print container_id
    new_req_body='{"Binds":["/tmp:/tmp"], "Links":[], "LxcConf":{"lxc.utsname":"docker"},"PortBindings":{ "22/tcp": [{ "HostPort": "11022" }] },"PublishAllPorts":false, "Privileged":false, "Dns": ["8.8.8.8"],"DnsSearch": [""],"VolumesFrom": ["parent", "other:ro"], "CapAdd": ["NET_ADMIN"], "CapDrop": ["MKNOD"],"RestartPolicy": { "Name": "", "MaximumRetryCount": 0 },"NetworkMode": "bridge","Devices": []}'
    new_conn.request("POST", "/containers/" + container_id + "/start" , new_req_body, headers)
    r1 = new_conn.getresponse().read()
    context={'name':r1,'name':container_id}
    return render(request,'finalapp/start_container.html',context)

@login_required
def ask_del_container(request):
    if request.user.is_authenticated:
        user=request.user.username
    if request.method == 'POST':
        container_id = request.POST['container_id']
        return HttpResponseRedirect('/finalapp/delete_container/'+(container_id)+'/')
    conn=httplib.HTTPConnection("localhost:4243")
    image_del='/containers/json?all=1'
    print image_del
    conn.request("GET",image_del)
    r2=conn.getresponse()
    print r2.status
    r2=json.loads(r2.read())
    image_id=[]
    for image in r2:
        image_id.append(image['Id'])
    context={'user':user,'image_id':image_id}
    return render(request,'finalapp/ask_del_container.html',context)
 
@login_required
def delete_container(request,container_id):
    container_id=container_id
    conn=httplib.HTTPConnection("localhost:4243")
    container_del='/containers/'
    container_del+=str(container_id)
    print container_del
    conn.request("DELETE",container_del)
    r2=conn.getresponse()
    print r2.status
    #print r1.read()
    #r1=r1.read()
    context={'container_id':container_id}
    return render(request, 'finalapp/delete_container.html', context)

@login_required
def ask_restart_container(request):
    if request.user.is_authenticated:
        user=request.user.username
    if request.method == 'POST':
        container_id = request.POST['container_id']
        return HttpResponseRedirect('/finalapp/restart_container/'+(container_id)+'/')
    conn=httplib.HTTPConnection("localhost:4243")
    image_del='/containers/json?all=1'
    print image_del
    conn.request("GET",image_del)
    r2=conn.getresponse()
    print r2.status
    r2=json.loads(r2.read())
    image_id=[]
    for image in r2:
        image_id.append(image['Id'])
    context={'user':user,'image_id':image_id}
    return render(request,'finalapp/ask_restart_container.html',context)
 
@login_required
def restart_container(request,container_id):
    container_id=container_id
    new_conn = httplib.HTTPConnection('localhost:4243')
    headers = {"Content-type": "application/json","Accept": "text/plain"}
    print container_id
    new_conn.request("POST", "/containers/" + container_id + "/restart?t=2", headers)
    r1 = new_conn.getresponse()
    print r1
    r1 = r1.read()
    print r1
    context={'name':r1}
    return render(request,'finalapp/restart_container.html',context)
