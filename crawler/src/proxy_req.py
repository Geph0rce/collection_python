#!/usr/bin/env python
# -*- coding:utf-8 -*-


from crawler_utils import parse_curl_str
# requests proxy demo
import requests


def use_lantern():
	# install lantern first, 这是使用lantern的代理地址
	proxies = {
		"http": "http://127.0.0.1:8787",
		"https": "http://127.0.0.1:8787",
	}

	url = 'http://httpbin.org/ip'
	r = requests.get(url, proxies=proxies)
	print(r.text)


def user_socks5():
	# requests from version 2.10.0 support socks proxy
	# pip install -U requests[socks]
	proxies = {'http': "socks5://myproxy:9191"}
	requests.get('http://example.org', proxies=proxies)

	# tornado proxy demo
	# sudo apt-get install libcurl-dev librtmp-dev
	# pip install tornado pycurl


def tornado_proxy():
	from tornado import httpclient, ioloop

	config = {
		'proxy_host': 'YOUR_PROXY_HOSTNAME_OR_IP_ADDRESS',
		'proxy_port': 3128
	}

	httpclient.AsyncHTTPClient.configure(
		"tornado.curl_httpclient.CurlAsyncHTTPClient")


	def handle_request(response):
		if response.error:
			print "Error:", response.error
		else:
			print response.body
		ioloop.IOLoop.instance().stop()

	http_client = httpclient.AsyncHTTPClient()
	http_client.fetch("http://twitter.com/",
		handle_request, **config)
	ioloop.IOLoop.instance().start()


def get_proxy_dict(ip, port, proxy_type='http' or 'socks5'):
    """get_proxy_dict return dict proxies as requests proxies
    http://docs.python-requests.org/en/master/user/advanced/

    :param ip: ip string
    :param port: int port
    :param proxy_type: 'http' or 'socks5'
    """
    proxies = {
        'http': '{proxy_type}://{ip}:{port}'.format(proxy_type=proxy_type, ip=ip, port=port),
        'https': '{proxy_type}://{ip}:{port}'.format(proxy_type=proxy_type, ip=ip, port=port),
    }
    return proxies


def requests_proxy(ip, port):
    proxies = get_proxy_dict(ip, port)
    url = 'http://httpbin.org/ip'
    r = requests.get(url, proxies=proxies, timeout=10)
    print(r.text)


def test_socks_proxy(url):
    from ua import random_ua
    PROXIES = {'http': 'socks5://127.0.0.1:9050',
               'https': 'socks5://127.0.0.1:9050'}
    s = """
    curl 'http://www.lagou.com/activityapi/icon/showIcon.json?callback=jQuery11130673730597542487_1469756732278&type=POSITION&ids=2034591%2C2147192%2C1899225%2C2112714%2C1993280%2C2107221%2C1980427%2C959204%2C1570458%2C1382996%2C2164841%2C1535725%2C2015991%2C1909703%2C1924731%2C1924585%2C1917417%2C1961327%2C1949207%2C1949217%2C1961114%2C1962767%2C1915882%2C1958811%2C1929575%2C1929708%2C1926524%2C1914752&_=1469756732279' -H 'Cookie: ctk=1469756728; JSESSIONID=006FA63ABE28DD910325F0A2B21D80DD; LGMOID=20160729094529-D8AB7E5EBC00B32D65F29DC499FDEEE0; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1469756733; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1469756733' -H 'X-Anit-Forge-Code: 0' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4' -H 'User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36' -H 'Accept: text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01' -H 'Referer: http://www.lagou.com/' -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' -H 'X-Anit-Forge-Token: None' --compressed
    """
    url, headers, data = parse_curl_str
    headers['User-Agent'] = random_ua
    r = requests.get(url, headers=headers, proxies=PROXIES)
    print(r.text)


if __name__ == '__main__':
    # requests_proxy('101.201.235.141', 8000)
    # requests_proxy('171.39.28.231', 8123)
    test_socks_proxy(url='http://www.lagou.com/jobs/1606717.html')
