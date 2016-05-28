# lmf2
有烧烤功能

# lmf
要装的程序


$ sudo apt-get update

$ sudo apt-get install feh ttf-wqy-zenhei samba-common-bin samba python3-rpi.gpio

$ sudo pip3 install pexpect aiohttp
sudo  aiohttp_jinja2




viewnior  fullscreen picture


如果想用全屏播放，参数是：-r
如果想用HDMI输出声音，参数是：-o hdmi，并且有个前提：/boot/config.txt 里面设置HDMI_DRIVER=2





image 和 imagetmb 增加图片 
image 1600*1200
imagetmb 200*150


文件名：排序xxx=菜名（不支持中文）_时间（秒）_视频文件名（视频要mp4结尾）.jpg(或png)

setting.txt
time1
time2up
time3dw
time4




    #file_object=open('p:/fse.txt','r')    # r只读，w可写，a追加
    #for line in file_object:
         #print(line)
    #file_object.close()




chromium

sudo leafpad /etc/apt/sources.list

复制add以下地址

deb http://mirrors.tuna.tsinghua.edu.cn/raspbian/raspbian/ wheezy main contrib non-free rpi 
deb-src http://mirrors.tuna.tsinghua.edu.cn/raspbian/raspbian/ wheezy main contrib non-free rpi 
deb http://mirrors.neusoft.edu.cn/raspbian/raspbian/ wheezy main contrib non-free rpi 
deb-src http://mirrors.neusoft.edu.cn/raspbian/raspbian/ wheezy main contrib non-free rpi 
deb http://mirrors.ustc.edu.cn/raspbian/raspbian/ wheezy main contrib non-free rpi 
deb-src http://mirrors.ustc.edu.cn/raspbian/raspbian/ wheezy main contrib non-free rpi



sudo apt-get install chromium-browser chromium-l10n

chromium-l10n这是中文语言包
In order to have a better display you can also install MC core fonts using 

sudo apt-get install ttf-mscorefonts-installer




可以直接在图形界面设置固定IP

sudo leafpad /etc/network/interfaces


iface eth0 inet static

address 192.168.1.105
netmask 255.255.255.0
gateway 192.168.1.1
