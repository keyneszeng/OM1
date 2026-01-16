# 手动模式

[General]
loglevel = info
logoutput = {{ logoutput }}
dns-server = 114.114.114.114, 223.5.5.5
routing-domain-resolve = true

# Local HTTP CONNECT proxy
interface = {{ lanInterface }}
port = {{ httpPort }}
# Local SOCKS5 CONNECT proxy
socks-interface = {{ lanInterface }}
socks-port = {{ socksPort }}

[Proxy]
Trojan = trojan, {{ address }}, {{ port }}, password={{ password }}, sni={{ sni }}

[Rule]
FINAL, Trojan
