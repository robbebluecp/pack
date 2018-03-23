import urllib.request
import time
import pthread
import random
import log
import gzip
import http.client
import urllib.error


def crawl(url, timeout=5, encoding='utf8', maxtime=5, isProxy=False, proxyConfig=None, crawlConfig=None, urlConfig=None,
          **kwargs):
    urlConfig_ = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0',
                  'Referer': '',
                  'Host': '',
                  'Cookie': ''}

    crawlConfig_ = {'timeout': timeout,
                    'encoding': encoding,
                    'maxtime': maxtime}

    protocol = url[:url.find(':')]

    if not urlConfig:
        urlConfig_.update(
            {x.replace('_', '-'): kwargs[x] for x in kwargs if 65 <= ord(str(x)[0]) <= 90 and kwargs[x] != ''})
    else:
        urlConfig_.update({x: urlConfig[x] for x in urlConfig if 65 <= ord(str(x)[0]) <= 90 and urlConfig[x] != ''})
    if not crawlConfig:
        crawlConfig_.update({x: kwargs[x] for x in kwargs if
                             type(kwargs[x]) == str and kwargs[x] is not None and x in ['maxtime', 'tiemout',
                                                                                        'encoding']})
    else:
        crawlConfig_.update({x: kwargs[x] for x in crawlConfig if
                             type(crawlConfig[x]) == str and crawlConfig[x] is not None and x in ['maxtime', 'tiemout',
                                                                                                  'encoding']})

    index = 0
    while index <= crawlConfig_['maxtime']:

        try:
            if isProxy:
                # 自动从代理池获取
                if not proxyConfig:
                    proxy = random.choice(pthread.proxyList)
                    proxyData = 'http://' + proxy
                else:
                    # proxyConfig = {'type': 1, 'proxyInfo': [your ips,type list]}
                    if str(proxyConfig['type']) == '1':  # 自定义代理池
                        proxyList = proxyInfo = proxyConfig['proxyInfo']
                        proxy = random.choice(proxyList)
                        proxyData = 'http://' + proxy
                    # proxyConfig = {'type': 2, 'proxyInfo':[{'host':'http-dyn.abuyun.com','port':'9020', 'user':'', 'password':''},{'host':'http-dyn.abuyun.com','port':'9020', 'user':'', 'password':''}]}
                    if str(proxyConfig['type']) == '2':  # abuyun代理
                        proxyInfo = proxyConfig['proxyInfo']
                        proxy = random.choice(proxyInfo)
                        user = proxyInfo['user']
                        password = proxyInfo['password']
                        host = proxyConfig['host']
                        port = proxyInfo['port']
                        proxyData = '%(user)s:%(password)s@%(host)s:%(port)s' % {'user': user, 'password': password,
                                                                                 'host': host, 'port': port}
                proxyHandler = urllib.request.ProxyHandler({protocol: proxyData})
                opener = urllib.request.build_opener(proxyHandler)
            else:
                opener = urllib.request.build_opener()


            try:
                rawHtml = opener.open(url, timeout=crawlConfig_['timeout'])
                if rawHtml.code != 200:
                    html = None
                    assert rawHtml.code == 200,'返回码%s不等于200,url:%s'% (rawHtml.code,url)
                else:
                    bytes = rawHtml.read()
                    try:
                        data = gzip.decompress(bytes)
                    except:
                        data = bytes
                    html = data.decode(crawlConfig_['encoding'], errors='ignore')
                    return html
            except http.client.BadStatusLine:
                index += 1
                log.critical('BadStatusLine Error, URL:' % url)
            except urllib.error.URLError as e:
                index += 0.2
                log.error('URLError, URL:%s, ERROR:%s' % (url, e))
            except Exception as e:
                log.error('Other Error, URL:%s, ERROR:%s'% (url, e))
            log.error('Index is over than %s times,crawl fail, URL;%s' % (crawlConfig_['maxtime'], url))
            return None
        except Exception as e:
            log.critical('...', e)
            return None
