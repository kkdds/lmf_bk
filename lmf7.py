#! /usr/bin/python3.4
# -*- coding: utf-8 -*-

import asyncio, os, json, time
from aiohttp import web
import aiohttp_jinja2
import jinja2
import urllib.request
from pyomxplayer import OMXPlayer
from qiv import QIV
import RPi.GPIO as GPIO

stapwd='abc'
setpwd='lmf2016'
softPath='/home/pi/lmf/'

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17, GPIO.OUT)#baowen
GPIO.setup(27, GPIO.OUT)#jia re guan
GPIO.setup(22, GPIO.OUT)#stream out
GPIO.setup(23, GPIO.OUT)#shao kao
GPIO.output(17, 1)
GPIO.output(27, 1)
GPIO.output(22, 1)
GPIO.output(23, 1)

#正转
GPIO.setup(5, GPIO.OUT)
#反转
GPIO.setup(6, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
#GPIO.PWM(channel, frequency)
p = GPIO.PWM(12, 50)
p.start(0)


@aiohttp_jinja2.template('index7.html')
def index(request):
    global shell_ud_t1_set,shell_ud_t2u_set,shell_ud_t2d_set,shell_ud_t3_set
    global softPath
    s = os.sep
    #rootpath = "image"    
    #root = "/home/pi/lmf/image"
    rootpath = "imagetmb"    
    root = softPath+"imagetmb"
    caifiles=[]
    for i in os.listdir(root):
        if os.path.isfile(os.path.join(root,i)):
            caiclass=i.split(".")[0]
            cainame=i.split(".")[1]
            dltime=i.split(".")[2]
            videoname=i.split(".")[3]            
            caifiles.append([i,caiclass,cainame,dltime,videoname])
            
    caifiles.sort()       
    file_object=open(softPath+'setting.txt','r')    # r只读，w可写，a追加    
    shell_ud_t1_set=int(file_object.readline())
    shell_ud_t2u_set=int(file_object.readline())
    shell_ud_t2d_set=int(file_object.readline())
    shell_ud_t3_set=int(file_object.readline())
    #for line in file_object:
         #print(line)         
    file_object.close()
            
    #使用aiohttp_jinja2  methed 2
    return {'test': '3', 'caifiles': caifiles}


omx=object
qviv=object
@asyncio.coroutine
def video(request):
    global omx,qviv
    global stapwd,setpwd,softPath

    po = yield from request.post()
    #print(po)
    #yield from playv(request)
    if po['p'] == stapwd:
        if po['m'] == 'play':        
            omx = OMXPlayer(softPath+'Videos/'+po['d']+'.mp4')
            tbody= '{"a":"video","b":"play"}'
            while omx._VOF:
                yield from asyncio.sleep(0.5)
            qviv=QIV(softPath+'/'+po['i'])

        elif po['m'] == 'stop':        
            omx.stop()
            tbody= '{"a":"video","b":"stop"}'
            qviv=QIV(softPath+'/'+po['i'])
        elif po['m'] == 'pause':        
            omx.toggle_pause()
            tbody= '{"a":"video","b":"pause"}'
    else:
        tbody= '{"p":"error"}'
        
    print(tbody)
    return web.Response(headers='' ,body=tbody.encode('utf-8'))

huixiqi=0
watchdog=0
eTimer1=False
eIntval1=5
eTimer2=False
eIntval2=8
sta_shell=0
sta_onoff=0
shell_up_down=0

shell_ud_t1_set=0
shell_ud_t2u_set=0
shell_ud_t2d_set=0
shell_ud_t3_set=0
shell_ud_t1=1
shell_ud_t2u=2
shell_ud_t2d=2
shell_ud_t3=1
'''
shell_sta
0 top stop
1 running
2 bottom stop

shell_up_down
0 to up
2 to bottom

running_sta
0 stop
1 running
'''

@asyncio.coroutine
def return_sta(request):
    global eTimer1,eIntval1,eTimer2,eIntval2,sta_shell,sta_onoff,watchdog
    global shell_up_down,shell_ud_t1,shell_ud_t2u,shell_ud_t2d,shell_ud_t3
    global stapwd,setpwd,softPath,tempeture_1

    hhdd=[('Access-Control-Allow-Origin','*')]
    po = yield from request.post()
    if po['p'] == stapwd:
        
        if po['m'] == 'login':            
            sta_shell=0
            sta_onoff=0
            tbody= '{"p":"ok"}'            
            return web.Response(headers=hhdd ,body=tbody.encode('utf-8'))
        
        elif po['m'] == 'sta':
            watchdog=0
            tbody= '{"shell_sta":'+str(sta_shell)+',"running_sta":'+str(sta_onoff)+',"tmp1":'+str(tempeture_1)+'}'
            return web.Response(headers=hhdd ,body=tbody.encode('utf-8'))
                
        elif po['m'] == 'gpioon':
            delaytime=po['t']
            if po['d']== 'fm':
                eTimer1=True
                eIntval1=int(time.time())+int(delaytime)
                print('eTimer1 1 start')
                sta_shell=1
                sta_onoff=1
                GPIO.output(22, 0)
                GPIO.output(27, 0)
                tbody= '{"a":"2227","b":"on"}'
            elif po['d']== 'fs':
                GPIO.output(17, 0)
                tbody= '{"a":"17","b":"on"}'
            elif po['d']== 'sk':
                GPIO.output(23, 0)
                tbody= '{"a":"23","b":"on"}'
            print(tbody)
            return web.Response(headers=hhdd ,body=tbody.encode('utf-8'))
                
        elif po['m'] == 'gpiooff':
            if po['d']== 'fm':
                sta_onoff=0
                GPIO.output(22, 1)
                GPIO.output(27, 1)
                tbody= '{"a":"2227","b":"off"}'
            elif po['d']== 'fs':
                GPIO.output(17, 1)
                tbody= '{"a":"17","b":"off"}'
            elif po['d']== 'sk':
                GPIO.output(23, 1)
                tbody= '{"a":"23","b":"off"}'
            print(tbody)
            return web.Response(headers=hhdd ,body=tbody.encode('utf-8'))
                
        elif po['m'] == 'shell':
            GPIO.output(5, 1)
            GPIO.output(6, 1)
            shell_ud_t1=shell_ud_t1_set
            shell_ud_t3=shell_ud_t3_set
            if po['d']== 'up' and sta_shell!=1:
                GPIO.output(6, 0)
                p.ChangeDutyCycle(40)
                shell_ud_t2u=shell_ud_t2u_set
                shell_ud_t2d=-1
                shell_up_down=0
                sta_shell=1
                tbody= '{"a":"shell","b":"up"}'
            elif po['d']== 'dw' and sta_shell!=1:
                GPIO.output(5, 0)
                p.ChangeDutyCycle(40)
                shell_ud_t2u=-1
                shell_ud_t2d=shell_ud_t2d_set
                shell_up_down=2
                sta_shell=1
                tbody= '{"a":"shell","b":"dw"}'
            elif sta_shell==1:
                sta_shell=2
                p.ChangeDutyCycle(0)
                tbody= '{"a":"shell","b":"stop"}'
            print(tbody)
            return web.Response(headers=hhdd ,body=tbody.encode('utf-8'))
        
    else:
        tbody= '{"p":"error"}'
        return web.Response(headers=hhdd ,body=tbody.encode('utf-8'))



@asyncio.coroutine
def setting(request):
    global shell_ud_t1_set,shell_ud_t2u_set,shell_ud_t2d_set,shell_ud_t3_set
    global stapwd,setpwd,softPath 

    hhdd=[('Access-Control-Allow-Origin','*')]
    po = yield from request.post()
    if po['m'] == 'r':
        #r+ 以读写模式打开 r只读，w可写，a追加
        file_object=open(softPath+'setting.txt','r+')
        shell_ud_t1_set=int(file_object.readline())
        shell_ud_t2u_set=int(file_object.readline())
        shell_ud_t2d_set=int(file_object.readline())
        shell_ud_t3_set=int(file_object.readline())
        file_object.close()
        tbody= '{"p":"ok","t1":"'+str(shell_ud_t1_set)+'","t2u":"'+str(shell_ud_t2u_set)+'","t2d":"'+str(shell_ud_t2d_set)+'","t3":"'+str(shell_ud_t3_set)+'"}'            
        return web.Response(headers=hhdd ,body=tbody.encode('utf-8'))

    if po['m'] == 'w' and po['p'] == setpwd:
        file_object=open(softPath+'setting.txt','r+')
        shell_ud_t1_set=int(po['t1'])
        shell_ud_t2u_set=int(po['t2u'])
        shell_ud_t2d_set=int(po['t2d'])
        shell_ud_t3_set=int(po['t3'])
        file_object.write(str(shell_ud_t1_set)+'\n')
        file_object.write(str(shell_ud_t2u_set)+'\n')
        file_object.write(str(shell_ud_t2d_set)+'\n')
        file_object.write(str(shell_ud_t3_set)+'\n')
        file_object.close()
        tbody= '{"p":"ok","w":"ok"}'            
        return web.Response(headers=hhdd ,body=tbody.encode('utf-8'))
        
    tbody= '{"p":"error"}'
    return web.Response(headers=hhdd ,body=tbody.encode('utf-8'))

SDI=2
SCS=3
SCK=4
GPIO.setup(SDI, GPIO.IN)
GPIO.setup(SCS, GPIO.OUT)
GPIO.setup(SCK, GPIO.OUT)
GPIO.output(SCS, 1)
GPIO.output(SCK, 0)
def SpiRead():
    i=0
    dt=0
    temp=[0,0,0]
    GPIO.output(SCS, 0)
    GPIO.output(SCS, 0)
    for i in range(32):
        GPIO.output(SCK, 1)
        GPIO.output(SCK, 1)		
        if(GPIO.input(SDI)==1):
            dt=dt<<1
            dt+=1
        else:
            dt=dt<<1
        GPIO.output(SCK, 0)
        GPIO.output(SCK, 0)
    GPIO.output(SCS, 1)
    temp[0]=dt>>18
    temp[1]=(dt & 0xffff)>>4
    temp[2]=dt & 0b1111
    if temp[2]!= 0:
        return 0
    else:
        return str(temp[0]/4)
        #return str(temp[1]/16)


tempeture_1=20
@asyncio.coroutine
def get_temp():
    global tempeture_1
    while True:
        yield from asyncio.sleep(1.5)        
        tempeture_1=SpiRead()
        #print(tempeture_1)


@asyncio.coroutine
def loop_info():
    global eTimer1,eIntval1,eTimer2,eIntval2,sta_shell,sta_onoff
    global watchdog,p
    global shell_up_down,shell_ud_t1,shell_ud_t2u,shell_ud_t2d,shell_ud_t3
    while True:
        yield from asyncio.sleep(0.05)
        watchdog+=1
        if watchdog>100:
            watchdog=0;
            sta_onoff=0
            print('watchdog')
            GPIO.output(17, 1)
            GPIO.output(22, 1)
            GPIO.output(23, 1)
            GPIO.output(27, 1)
                    
        if eTimer1==True:
            #sta_shell=1
            if int(time.time())>=int(eIntval1):
                print('eTimer1 1 end')
                GPIO.output(22, 1)
                GPIO.output(27, 1)
                eTimer1=False
                sta_shell=2
                sta_onoff=0
                
        #if shell_up_down != 0:
        if sta_shell==1:
            #sta_shell=1
            if shell_ud_t1 > 0:
                shell_ud_t1-=1
            elif shell_ud_t1 == 0:
                p.ChangeDutyCycle(95)
                shell_ud_t1 =-1
            elif shell_ud_t2u > 0:
                shell_ud_t2u-=1
            elif shell_ud_t2u == 0:
                p.ChangeDutyCycle(10)
                shell_ud_t2u =-1
            elif shell_ud_t2d > 0:
                shell_ud_t2d-=1
            elif shell_ud_t2d == 0:
                p.ChangeDutyCycle(10)
                shell_ud_t2d =-1
            elif shell_ud_t3 > 0:
                shell_ud_t3-=1
            elif shell_ud_t3 == 0:
                shell_ud_t3 =-1
                p.ChangeDutyCycle(0)
                if shell_up_down == 0:
                    sta_shell=0
                elif shell_up_down == 2:
                    sta_shell=2
                print('shell run end '+str(sta_shell))

        else: # shell_up_down==0
            shell_up_down=0
            #p.stop()
    return 1


@asyncio.coroutine
def init(loop):    
    global softPath
    app = web.Application(loop=loop)    
    #使用aiohttp_jinja2
    aiohttp_jinja2.setup(app,loader=jinja2.FileSystemLoader('/home/pi/lmf/templates'))
    
    app.router.add_route('*', '/', index)
    app.router.add_route('*', '/video', video)
    app.router.add_route('POST', '/sta', return_sta)
    app.router.add_route('POST', '/setting', setting)
    app.router.add_static('/css',  softPath+'css')
    app.router.add_static('/js',  softPath+'js')
    app.router.add_static('/image',  softPath+'image')
    app.router.add_static('/imagetmb', softPath+'imagetmb')
    srv = yield from loop.create_server(app.make_handler(), '0.0.0.0', 9001)
    print(' v7 server started at http://0.0.0.0:9001...')               
    return srv

loop = asyncio.get_event_loop()
tasks = [init(loop), loop_info(), get_temp()]#loop_info持续发送状态
loop.run_until_complete(asyncio.wait(tasks))
loop.run_forever()
