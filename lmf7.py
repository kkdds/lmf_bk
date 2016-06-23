#! /usr/bin/python3.4
# -*- coding: utf-8 -*-

import asyncio, os, json, time
import aiohttp_jinja2
import jinja2
import urllib.request
import RPi.GPIO as GPIO
from aiohttp import web
from pyomxplayer import OMXPlayer
#from qiv import QIV
from urllib.parse import unquote
import configparser

stapwd='abc'
setpwd='lmf2016'
softPath='/home/pi/lmf/'

kconfig=configparser.ConfigParser()
kconfig.read(softPath+"setting.ini")
shell_ud_t1_set=kconfig.getint("yp","shell_ud_t1_set")
shell_ud_t2u_set=kconfig.getint("yp","shell_ud_t2u_set")
shell_ud_t2d_set=kconfig.getint("yp","shell_ud_t2d_set")
shell_ud_t3_set=kconfig.getint("yp","shell_ud_t3_set")
shell_sdu = kconfig.getint("yp","shell_sdu")
shell_sdd = kconfig.getint("yp","shell_sdd")
stapwd = kconfig.get("yp","stapwd")

seled_cai=[]

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
io_sk=7 #烧烤
io_jr=8 #加热管
io_zq=25 #蒸汽
io_bw=24 #保温
io_hx=23 #回吸
io_e2=18 #
io_e3=15 #
io_e4=14 #
GPIO.setup(io_bw, GPIO.OUT)
GPIO.setup(io_jr, GPIO.OUT)
GPIO.setup(io_zq, GPIO.OUT)
GPIO.setup(io_sk, GPIO.OUT)
GPIO.setup(io_hx, GPIO.OUT)
GPIO.setup(io_e2, GPIO.OUT)
GPIO.setup(io_e3, GPIO.OUT)
GPIO.setup(io_e4, GPIO.OUT)
GPIO.output(io_bw, 1)
GPIO.output(io_jr, 1)
GPIO.output(io_zq, 1)
GPIO.output(io_sk, 1)
GPIO.output(io_hx, 1)
GPIO.output(io_e2, 1)
GPIO.output(io_e3, 1)
GPIO.output(io_e4, 1)

moto_1_p=13 #脉宽输出
moto_1_f=19 #正转
moto_1_r=26 #反转
GPIO.setup(moto_1_f, GPIO.OUT)
GPIO.setup(moto_1_r, GPIO.OUT)
GPIO.setup(moto_1_p, GPIO.OUT)
p = GPIO.PWM(moto_1_p, 50)
p.start(0)

moto_2_p=21 #脉宽输出
moto_2_f=20 #正转
moto_2_r=16 #反转
GPIO.setup(moto_2_f, GPIO.OUT)
GPIO.setup(moto_2_r, GPIO.OUT)
GPIO.setup(moto_2_p, GPIO.OUT)
p2 = GPIO.PWM(moto_2_p, 50)
p2.start(0)

huixiqi=0
watchdog=0
eTimer1=False
eIntval1=5
eTimer2=False
eIntval2=8
sta_shell=0
sta_onoff=0
shell_up_down=0

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

@aiohttp_jinja2.template('index1.html')
def index1(request):
    #使用aiohttp_jinja2  methed 2
    return {'test': '3', 'caifiles': 'y'}


@aiohttp_jinja2.template('index2.html')
def index2(request):
    global shell_ud_t1_set,shell_ud_t2u_set,shell_ud_t2d_set,shell_ud_t3_set
    global softPath,seled_cai
    s = os.sep
    #rootpath = "image"    
    #root = "/home/pi/lmf/image"
    rootpath = "imagetmb"    
    root = softPath+"imagetmb"
    caifiles=[]
    #seled_cai=[]
    for i in os.listdir(root):
        if os.path.isfile(os.path.join(root,i)):
            caiclass=i.split(".")[0]
            bigimg=i.split(".")[1]
            cainame=unquote(i.split(".")[4])
            dltime=i.split(".")[2]
            videoname=i.split(".")[3]

            #seled_cai.index(i)
            try:
                seled_cai.index(i)
            except:
                cseled=''
            else:
                cseled='myselcai'

            caifiles.append([i,caiclass,cainame,dltime,videoname,bigimg,cseled])
            
    caifiles.sort()
    #使用aiohttp_jinja2  methed 2
    return {'test': '3', 'caifiles': caifiles}


@aiohttp_jinja2.template('index3.html')
def index3(request):
    global shell_ud_t1_set,shell_ud_t2u_set,shell_ud_t2d_set,shell_ud_t3_set
    global softPath,seled_cai
    s = os.sep
    rootpath = "imagetmb"    
    root = softPath+"imagetmb"
    caifiles=[]
    for i in seled_cai:
        if 1:
            caiclass=i.split(".")[0]
            bigimg=i.split(".")[1]
            cainame=unquote(i.split(".")[4])
            dltime=i.split(".")[2]
            videoname=i.split(".")[3]            
            caifiles.append([i,caiclass,cainame,dltime,videoname,bigimg])
            
    caifiles.sort()
    #使用aiohttp_jinja2  methed 2
    return {'test': '3', 'caifiles': caifiles}


@aiohttp_jinja2.template('set.html')
def setpage(request):
    #global shell_ud_t1_set,shell_ud_t2u_set,shell_ud_t2d_set,shell_ud_t3_set
    #global softPath
    shell_ud_t1_set=kconfig.getint("yp","shell_ud_t1_set")
    shell_ud_t2u_set=kconfig.getint("yp","shell_ud_t2u_set")
    shell_ud_t2d_set=kconfig.getint("yp","shell_ud_t2d_set")
    shell_ud_t3_set=kconfig.getint("yp","shell_ud_t3_set")
    shell_sdu = kconfig.getint("yp","shell_sdu")
    shell_sdd = kconfig.getint("yp","shell_sdd")
    stapwd = kconfig.get("yp","stapwd")
    s_arr = {"t1":str(shell_ud_t1_set),"t2u":str(shell_ud_t2u_set)}
    s_arr['t2d'] = str(shell_ud_t2d_set)
    s_arr['t3'] = str(shell_ud_t3_set)
    s_arr['sdu'] = str(shell_sdu)
    s_arr['sdd'] = str(shell_sdd)
    s_arr['stapwd'] = stapwd
    #print(s_arr)
    #使用aiohttp_jinja2  methed 2
    #return {"p":"ok","t1":str(shell_ud_t1_set),"t2u":str(shell_ud_t2u_set),"t2d":str(shell_ud_t2d_set),"t3":str(shell_ud_t3_set)}
    return {"p":"ok","r":s_arr}


omx=object
@asyncio.coroutine
def video(request):
    global omx
    global stapwd,setpwd,softPath

    po = yield from request.post()
    if 1:#po['p'] == stapwd:
        if po['m'] == 'play':
            #print('video play...')    
            omx = OMXPlayer(softPath+'Videos/'+po['d']+'.mp4',softPath+po['i'])
            tbody= '{"a":"video","b":"play"}'

        elif po['m'] == 'stop':        
            omx.stop()
            tbody= '{"a":"video","b":"stop"}'

        elif po['m'] == 'pause':        
            omx.toggle_pause()
            tbody= '{"a":"video","b":"pause"}'
    else:
        tbody= '{"p":"error"}'
        
    print(tbody)
    return web.Response(headers='' ,body=tbody.encode('utf-8'))

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
                GPIO.output(io_zq, 0)
                GPIO.output(io_jr, 0)
                tbody= '{"a":"zq+jr","b":"on"}'
            elif po['d']== 'fs':
                GPIO.output(io_bw, 0)
                tbody= '{"a":"bw","b":"on"}'
            elif po['d']== 'sk':
                GPIO.output(io_sk, 0)
                tbody= '{"a":"sk","b":"on"}'
            elif po['d']== 'ms':
                GPIO.output(io_zq, 0)
                GPIO.output(io_jr, 0)
                tbody= '{"a":"ms","b":"on"}'
            print(tbody)
            return web.Response(headers=hhdd ,body=tbody.encode('utf-8'))
                
        elif po['m'] == 'gpiooff':
            if po['d']== 'fm':
                sta_onoff=0
                GPIO.output(io_zq, 1)
                GPIO.output(io_jr, 1)
                tbody= '{"a":"zq+jr","b":"off"}'
            elif po['d']== 'fs':
                GPIO.output(io_bw, 1)
                tbody= '{"a":"bw","b":"off"}'
            elif po['d']== 'sk':
                GPIO.output(io_sk, 1)
                tbody= '{"a":"sk","b":"off"}'
            elif po['d']== 'ms':
                GPIO.output(io_zq, 1)
                GPIO.output(io_jr, 1)
                tbody= '{"a":"ms","b":"off"}'
            print(tbody)
            return web.Response(headers=hhdd ,body=tbody.encode('utf-8'))
                
        elif po['m'] == 'shell':
            GPIO.output(moto_1_f, 1)
            GPIO.output(moto_1_r, 1)
            shell_ud_t1=shell_ud_t1_set
            shell_ud_t3=shell_ud_t3_set
            if po['d']== 'up' and sta_shell!=1:
                GPIO.output(moto_1_r, 0)
                p.ChangeDutyCycle(40)
                shell_ud_t2u=shell_ud_t2u_set
                shell_ud_t2d=-1
                shell_up_down=0
                sta_shell=1
                tbody= '{"a":"shell","b":"up"}'
            elif po['d']== 'dw' and sta_shell!=1:
                GPIO.output(moto_1_f, 0)
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
                
        elif po['m'] == 'pump2':
            GPIO.output(moto_2_f, 0)
            GPIO.output(moto_2_r, 1)
            p2.ChangeDutyCycle(int(po['spd']))
            tbody= '{"a":"pump2","b":"'+po['spd']+'"}'
            print(tbody)
            return web.Response(headers=hhdd ,body=tbody.encode('utf-8'))
        
    else:
        tbody= '{"p":"error"}'
        return web.Response(headers=hhdd ,body=tbody.encode('utf-8'))



@asyncio.coroutine
def setting(request):
    global shell_ud_t1_set,shell_ud_t2u_set,shell_ud_t2d_set,shell_ud_t3_set
    global shell_sdu,shell_sdd
    global stapwd,setpwd,softPath,seled_cai
    hhdd=[('Access-Control-Allow-Origin','*')]
    tbody= '{"p":"error"}'

    po = yield from request.post()
    if po['m'] == 'l' and po['p'] == setpwd:
        tbody= '{"p":"ok"}'
        return web.Response(headers=hhdd ,body=tbody.encode('utf-8'))

    if po['m'] == 'w' and po['p'] == setpwd:
        shell_ud_t1_set=po['t1']
        shell_ud_t2u_set=po['t2u']
        shell_ud_t2d_set=po['t2d']
        shell_ud_t3_set=po['t3']
        shell_sdu=po['sdu']
        shell_sdd=po['sdd']
        stapwd=po['stapwd']
        kconfig.set("yp","shell_ud_t1_set",str(shell_ud_t1_set))
        kconfig.set("yp","shell_ud_t2u_set",str(shell_ud_t2u_set))
        kconfig.set("yp","shell_ud_t2d_set",str(shell_ud_t2d_set))
        kconfig.set("yp","shell_ud_t3_set",str(shell_ud_t3_set))
        kconfig.set("yp","shell_sdu",str(shell_sdu))
        kconfig.set("yp","shell_sdd",str(shell_sdd))
        kconfig.set("yp","stapwd",stapwd)
        kconfig.write(open(softPath+"setting.ini","w"))
        tbody= '{"p":"ok","w":"ok"}'
        return web.Response(headers=hhdd ,body=tbody.encode('utf-8'))

    if po['m'] == 'addcai':
        if po['s'] == 'true':  
            seled_cai.remove(po['c'])
            #print(seled_cai)
            tbody= '{"p":"dec"}'
        else:
            seled_cai.append(po['c'])
            #print(seled_cai)
            tbody= '{"p":"add"}'
        
    #tbody= '{"p":"error"}'
    return web.Response(headers=hhdd ,body=tbody.encode('utf-8'))


from w1thermsensor import W1ThermSensor
tempeture_1=0
@asyncio.coroutine
def get_temp():
    global tempeture_1
    while True:
        yield from asyncio.sleep(1.5)        
        #tempeture_1=SpiRead()
        for sensor in W1ThermSensor.get_available_sensors():
            tempeture_1=sensor.get_temperature()


@asyncio.coroutine
def loop_info():
    global eTimer1,eIntval1,eTimer2,eIntval2,sta_shell,sta_onoff
    global watchdog,huixiqi,p
    global shell_up_down,shell_ud_t1,shell_ud_t2u,shell_ud_t2d,shell_ud_t3
    while True:
        yield from asyncio.sleep(0.05)
        watchdog+=1
        if watchdog>100:
            watchdog=0;
            sta_onoff=0
            print('watchdog')
            GPIO.output(io_bw, 1)
            GPIO.output(io_jr, 1)
            GPIO.output(io_zq, 1)
            GPIO.output(io_sk, 1)
            GPIO.output(io_hx, 1)
            
        if huixiqi>0:
            huixiqi-=1;            
        else:
            #huixiqi=0
            GPIO.output(io_hx, 1)
                   
        if eTimer1==True:
            #sta_shell=1
            if int(time.time())>=int(eIntval1):
                print('eTimer1 1 end')
                GPIO.output(io_jr, 1)
                GPIO.output(io_zq, 1)
                eTimer1=False
                sta_shell=2
                sta_onoff=0
                huixiqi=120
                GPIO.output(io_hx, 0)
                print('huixiqi on')
                
        #if shell_up_down != 0:
        if sta_shell==1:
            #sta_shell=1
            if shell_ud_t1 > 0:
                shell_ud_t1-=1
            elif shell_ud_t1 == 0:
                p.ChangeDutyCycle(65)
                shell_ud_t1 =-1
            elif shell_ud_t2u > 0:
                shell_ud_t2u-=1
            elif shell_ud_t2u == 0:
                p.ChangeDutyCycle(shell_sdu)
                shell_ud_t2u =-1
            elif shell_ud_t2d > 0:
                shell_ud_t2d-=1
            elif shell_ud_t2d == 0:
                p.ChangeDutyCycle(shell_sdd)
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
    
    app.router.add_route('*', '/', index1)
    app.router.add_route('*', '/index2', index2)
    app.router.add_route('*', '/index3', index3)
    app.router.add_route('*', '/set', setpage)
    app.router.add_route('*', '/video', video)
    app.router.add_route('POST', '/sta', return_sta)
    app.router.add_route('POST', '/setting', setting)
    app.router.add_static('/css',  softPath+'css')
    app.router.add_static('/js',  softPath+'js')
    app.router.add_static('/image',  softPath+'image')
    app.router.add_static('/imagetmb', softPath+'imagetmb')
    srv = yield from loop.create_server(app.make_handler(), '0.0.0.0', 9001)
    print(' v8 server started at http://0.0.0.0:9001...')               
    return srv

loop = asyncio.get_event_loop()
tasks = [init(loop), loop_info(), get_temp()]#loop_info持续发送状态
loop.run_until_complete(asyncio.wait(tasks))
loop.run_forever()
