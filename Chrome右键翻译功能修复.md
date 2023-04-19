# 信源	https://github.com/feliscatus/switchyomega/issues/264

## 思路1（目前理论最优）	代理工具TCP转发方法

1) hosts文件中配置
translate.google.com        127.0.0.1
translate.googleapis.com    127.0.0.1

2) 修改v2ray配置

	{
	"protocol": "tunnel",
	"local_address": "127.0.0.1",
	"local_port": 443,
	"forward_address": "translate.googleapis.com",
	"forward_port": 443,
	"mode": "tcp_only"
	}
	
## 思路2	Chrome命令行带代理配置启动方法

	#浏览器使用pac代理 
	chromium  --proxy-pac-url="http://localhost:8000/proxy.pac"
	#浏览器使用http代理
	chromium  --proxy-server="http=127.0.0.1:1087;https=127.0.0.1:1087"
	#浏览器使用socks5代理
	chromium --proxy-server="socks5://127.0.0.1:1080"--host-resolver-rules="MAP * ~NOTFOUND , EXCLUDE 127.0.0.1"
	
## 思路3	DNS拦截方法

	* 建立本地服务 dnsmasq nginx socat
	
	* dnsmasq 设置: address=/translate.googleapis.com/[nginx-ip]
	
	* nginx 设置: stream{server{listen:443;proxy_pass [socat-ip]:[socat-port];}}
	
	* socat 命令:  socat TCP-LISTEN:[port],fork SOCKS4a:[SOCKS-ip]:translate.googleapis.com:443,socksport=[SOCKS-port]
	
	* 设备的dns改为[dnsmasq-ip]
	
## 思路4	代理工具方法（损失性能）

	v2ray全局代理
	或者
	proxifier筛选translate.googleapis.com请求走代理
	
## 思路5（超级简单）	插件翻译方法
	
chrome插件"沉浸式翻译"
