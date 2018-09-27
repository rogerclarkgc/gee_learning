# 在windows7上搭建GEE本地运行环境

Google earth engine 是Google公司开发的一款GIS应用平台，它提供了多种在线的影像集合数据库，网页版本基于Javascript的API使用简便，文档十分详细，其强大而又高效的分析功能正受到越来越多的关注。

GEE也有本地化的基于Docker的运行环境，提供Python2.7下的API，给不熟悉Javascript的同学提供了一些便利。但由于其生产环境是通过Docker部署的，在没接触过的人看来有一些难度，再加上Docker对Win10以下的系统支持较差，Google官方的文档也较简单，甚至有错误，本文将记录自己搭建的过程和经验，希望使用GEE的人能从这里得到帮助。

本文使用SS+SSTAP的方案来解决连接GOOGLE服务的稳定性问题，经过测试，这样能很稳定的使用datalab

## 工具准备

为了完成GEE的本地化部署，需要准备如下软件工具

1. Docker toolbox for windows

	Docker官方建议在Win10上使用Docker，但他们也提供了兼容老版本Windows的工具。

	[下载](https://download.docker.com/win/stable/DockerToolbox.exe)

2. Github账号

	对于学生，Github education提供一份免费的服务支持(Student Developer Pack)，包括一张价值50美金的Digital Ocean公司的VPS兑换券。有了这张券，可以租用一个VPS用于搭建一个稳定的私有Shadowsocks服务器。（注：由于本服务被人滥用，Github近期加强了审核，需要提供学生证或学位照片作为学生证明。 作者于17年申请成功过，基本信息正确半天就可以通过，不知现在申请通过时间
	
	[申请链接](https://education.github.com/pack/)

3. Google账号

	用来连接google服务 

4. 一台VPS

	用于搭建Shadowsocks服务端，提高连接GOOGLE服务的稳定性。如何搭建将在后文给出

5. SSTAP

	这个软件用于辅助Shadowsocks客户端，它能将SS虚拟一张网卡，让电脑通过这个网卡上网，从而拦截所有网络请求，真正达到全局翻墙。让拉取Docker镜像的过程畅通无阻

	[下载](https://www.sockscap64.com/zh-hant/sstap/)

6. Putty

	用于远程操纵VPS，有时需要更改SS服务端的设置，就通过这个软件登陆VPS来操作

	[下载](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html)

7. （备选）SS客户端

	用于提供网页下的SS连接环境，在不想全局浏览时使用。

	[下载](https://github.com/shadowsocks/shadowsocks-windows/releases)

## 第一步：建立SS服务端

网上其实有许多免费的SS账号分享，但免费的总不如自己花钱的买的，自己搭建SS服务，不限流，保证稳定。

常见的国外VPS有[Digtal ocean](https://www.digitalocean.com)、[Vultr](https://www.vultr.com/)、[Bandwagon](https://bandwagonhost.com)，这三个里面Bandwagon最便宜（最低约2刀/月），但他的机房基本分布在北美，因此相对来说选择较少。 Digital ocean和Vultr相对较贵（最低5刀/月），但它们机房较多，大家可以选择离自己最近和延迟最低的机房。

作者使用过Digital ocean和Vultr的VPS，如果前面的Github student pack 申请通过，可以直接考虑Digital Ocean的VPS。本文就以这个公司为例子

1. 注册Digital Ocean

	[注册链接](https://www.digitalocean.com)

	DO和Github的账号可以联用，因此这一步很简单

2. 打钱

	DO支持paypal，国内的银联卡都支持paypal支付，如果没有paypal可以考虑Vultr的VPS，他们支持使用支付宝，十分方便。具体设置过程和DO基本一样。

3. 建立VPS

	在建VPS前，最好进行测速，[测速地址](http://speedtest-sfo1.digitalocean.com/)，看看自己所在地区与那个机房通信速度最快，延迟最低

	![SPEEDTEST](https://i.imgur.com/pDXUNQh.png)

	建立VPS过程很简单，只要跟着步骤一步步走就行了。

	这里选择最便宜的5刀一月的就够用了
	![S](https://i.imgur.com/9Qm7CoE.png)


	![SELETCVPS](https://i.imgur.com/OQ1b48k.png)


4. 通过putty登陆VPS

	VPS建立好后，登陆VPS的root用户密码会通过邮件发给到注册邮箱中，可以通过VPS供应商的网页终端登入，不过更常用的是使用自己的putty或其他终端

	![putty](https://i.imgur.com/9hiilLC.png)

	在登陆时，可以把登陆的IP存成配置文件，下次直接导入就可以了。
	登入时使用root权限，密码是VPS提供给你的密码，输入时终端不会有任何显示，注意不要输错。
	

	初次登陆后，需要设置root密码，在终端输入
	
			sudo passwd root
	
	两次键入密码就可以设置root密码，这样你就可以以root用户来操作VPS，很多命令需要的前置命令`su`也可使用了。
	
	当然，可以通过生成配对的SSH密匙来免密登陆，更安全，可以看[这里](https://blog.csdn.net/happyhuirong/article/details/41729911)

5. 使用脚本自动部署SS服务端

	手动编译SS服务端不失为一个学习技术的好方法，但为了更快的开始使用GEE，推荐使用大神们已经为你写好的自动化部署脚本，只要下载好脚本，按下回车，输入一些参数，几分钟后你的个人VPS就部署好了。

	以下的步骤都是在前面建立好的VPS上进行，这里使用的是[Teddysun](https://github.com/teddysun/shadowsocks_install)提供的脚本，这个脚本需要在root用户下运行。

		wget --no-check-certificate -O shadowsocks.sh https://raw.githubusercontent.com/teddysun/shadowsocks_install/master/shadowsocks.sh
		chmod +x shadowsocks.sh
		./shadowsocks.sh 2>&1 | tee shadowsocks.log

	按照脚本的指示一一设置就可以了。如果需要更改SS的设置，那么需要更改如下文件：`/etc/shadowsocks.json`，bash终端里比较简单的编辑器是`nano`，使用命令`nano /etc/shadowsocks.json`来打开并编辑。

		{
	    "server":"0.0.0.0",
	    "server_port":your_server_port,
	    "local_address":"127.0.0.1",
	    "local_port":1080,
	    "password":"your_password",
	    "timeout":300,
	    "method":"your_encryption_method",
	    "fast_open": false
		}

	一般来说，以上信息都会在执行完安装脚本后自动填好，有时需要更改VPS的端口`server_port`以及客户端的端口`local_port`，此外，加密方式`method`和`password`也是经常需要更改的。

	几条常见的命令可以用来管理VPS的SS服务

		启动：/etc/init.d/shadowsocks start
		停止：/etc/init.d/shadowsocks stop
		重启：/etc/init.d/shadowsocks restart
		状态：/etc/init.d/shadowsocks status

	要成功执行以上命令，需要确保权限为root。另外，也有几个常见的命令来管理VPS的网络连接

		#输出VPS当前所有的活动的udp和tcp网络连接
		netstat -a -u -t

6. 通过SSTAP连接SS服务端

	在配置好SS服务端后，使用SSTAP来做全局代理，只需要填入SS服务端的几条信息就可完成：

	![sstap](https://i.imgur.com/OAxdHnP.png)

	* 服务器IP：即VPS自身的IP，服务商会告诉你
	* 端口：即`shadowsocks.json`文件中`server_port`对应的数值
	* 密码：即`shadowsocks.json`文件中`password`对应的数值
	* 加密方式：即`shadowsocks.json`文件中`method`对应的数值

	填完后即可连接，这是在VPS中运行`netstat -a -u -t`就可以看到自己的VPS的端口与一个地址建立了连接，而这个地址就是你的IP地址

## 第二步 部署GEE的Docker环境

1. 安装Docker
	
	首先安装`Docker Toolbox`，安装的时候其实可以发现，`Docker Toolbox`帮你安装了`VirtualbBox`，这说明Docker容器其实并没有运行在你的Win7系统上，而是运行在Win7上的一个虚拟机里，这个问题会导致后面的端口映射错误的麻烦。
	
	在安装完成后，需要先运行`Docker Quikstart Terminal`来初始化Linux虚拟机，初始完成后，会打开Docker的终端，屏幕将输出这个Linux虚拟机的IP，这个IP很重要，需要记下
	
	![docker](https://i.imgur.com/YvgePSg.png)

2. 部署GEE

	GEE本地安装在GEE的[官方文档](https://developers.google.com/earth-engine/python_install-datalab-local)上有详细介绍，但这份文档是建立在Win10基础上的，而Win10的HyperV与系统整合更好，不像Win7，Docker仍然在Linux虚拟机上运行，因此，部分代码需要更改。

	首先，在`cmd`终端中初始化Docker容器，这一步可以按照GEE文档中来
	
		set "GCP_PROJECT_ID=YOUR_PROJECT_ID"
		set "CONTAINER_IMAGE_NAME=gcr.io/earthengine-project/datalab-ee:latest"
		set "HOME=%HOMEDRIVE%%HOMEPATH%"
		set "WORKSPACE=%HOME%\workspace\datalab-ee"
		mkdir "%WORKSPACE%"
		cd %WORKSPACE%

	接下来，拉取GEE镜像并在刚刚建立的容器中运行，由于我们前面让SSTAP代理了电脑的全局网络，这时所有网络请求都由SS代理，所以这时拉取过程不会有连接不上的情况，接下来这一步就与GEE教程中不同了

		docker run -it -p "8081:8080" -v "%WORKSPACE%:/content" -e "PROJECT_ID=%GCP_PROJECT_ID%" %CONTAINER_IMAGE_NAME%

	然后在浏览器输入前面记下的虚拟机地址加上`8081`端口，就可访问GEE datalab了

		http://192.168.99.100:8081
	
	这一步需要去掉`127.0.0.1`，因为`docker -p`是一个端口转发命令，`docker -p "127.0.0.1:8081:8080"`让docker容器中`127.0.0.1:8081`端口转发到宿主机的`8080`端口上，这样的初衷是实现通过宿主机来访问容器，但由于win7下的docker本身运行在一个linux虚拟机上，所以访问docker的实质是访问虚拟机，而`127.0.0.1`被默认为机器的本机地址，所以在浏览器中输入这个地址时会访问宿主机的基地址而非虚拟机的，这时如果本机的`8081`端口没开放访问，那么是一定会报错的。

	如果将前面的`127.0.0.1`去掉，就相当于虚拟机的所有地址都通过`8081`端口映射到宿主机的`8080`端口，这时只要在浏览器中输入虚拟机的ip加上刚刚`8081`端口就可访问。

3. 认证datalab权限

	认证权限的过程写在`/datalab/docs-earthengine/`的`authorize_notebook_server.ipynb`文件中，如果前面SS服务建立好了，认证过程也应该是畅通无误的。

	![AUTH](https://i.imgur.com/OHzyIyF.png)

	认证完毕，试一试是否能取回GEE的数据

	![TE](https://i.imgur.com/EHadQZZ.png)


