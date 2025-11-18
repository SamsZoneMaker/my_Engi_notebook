swpedia_keyword: [Baikal使用方法]

author:  desen.li@wisewavetech.com

------

# baikal简介

baikal（贝加尔湖）是arch专用的一台编译服务器（compilation server），位置在珠海IT机房红区

，其型号为h3c UniServer R4950，是红区内开发专用的编译方式。

## Baikal登入方法

1. 在红区内使用SSH连接工具，可以使用sshfs、winfsp或MobaXterm，这些工具可以在红区内的共享目录找到
```
\\wisewave.local\fs\rd\Engineering\Firmware\Eevelopment Environment\tools
```

2. 由于sshfs和winfsp均需要管理员安装（有需要可以找Bruce），以下以MobaXterm为例记录登入方法
   - 点击软件内的 “Session” → “SSH” 
   - 在Remote host中填入`10.1.3.228`，这是在linux中登入baikal的ip地址；后勾选Specify Username并填入OA账号，其他设置无需更改，点击 “OK”
   - 进入指令行窗口输入OA账号密码
   - 首次登入会要求设置master password，此密码为高级密码，当登入密码忘记时可以使用改高级密码重置

## 首次登入后的操作

分别执行下述指令

```
cd
mkdir .vnc
cp /arch/all/.bashrc .
cp /arch/all/.profile .
cp /arch/all/xstartup .vnc/
```

其中/arch下的共享目录为

```
1. /arch/all
	arch team共享
2. /arch/artemis
	artemis项目共享
3. /arch/mutant
	mutant项目共享
4. /arch/phoenix
	phoenix项目共享
5. /arch/songshan
	songshan项目共享
```
