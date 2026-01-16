# 全局模式

[General]
loglevel = info
logoutput = {{ logoutput }}
dns-server = 114.114.114.114, 223.5.5.5
routing-domain-resolve = true
always-real-ip = apple.com

# Local HTTP CONNECT proxy
interface = {{ lanInterface }}
port = {{ httpPort }}
# Local SOCKS5 CONNECT proxy
socks-interface = {{ lanInterface }}
socks-port = {{ socksPort }}

[Proxy]
Trojan = trojan, {{ address }}, {{ port }}, password={{ password }}, sni={{ sni }}
DirectLan = direct

[Rule]
# LAN
DOMAIN-SUFFIX, local, DirectLan
DOMAIN-SUFFIX, test, DirectLan
IP-CIDR, 127.0.0.0/8, DirectLan
IP-CIDR, 172.16.0.0/12, DirectLan
IP-CIDR, 192.168.0.0/16, DirectLan
IP-CIDR, 10.0.0.0/8, DirectLan
IP-CIDR, 17.0.0.0/8, DirectLan
IP-CIDR, 100.64.0.0/10, DirectLan
IP-CIDR, 224.0.0.0/4, DirectLan
IP-CIDR6, fe80::/10, DirectLan

FINAL, Trojan
