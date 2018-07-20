import urllib.request
import time
import random
try:
    import log
except:
    from . import log
import gzip
import http.client
import urllib.error



def crawl(url, timeout=5, encoding='utf8', maxtime=5, isProxy=False, proxyConfig=None, crawlConfig=None, urlConfig=None,
          **kwargs):
    """
    :param url:         :           Destination crawl url
    :param timeout:     :           Time delay to request a url
    :param encoding:    :           Decode method to decode the cource code of a url, like 'utf8','gbk' etc
    :param maxtime:     :           The max time to try to get response from each request.
                                     During the whole cycle in "while index <= crawlConfig_['maxtime']" , while fail(generally comes up exception) getting correct response,
                                     index will add 1 and programme will return None until index squal to maxtime.
    :param proxyConfig: :           If isProxy but with None in  proxyConfig, this means you have your own ip pools and get random proxy from ip pools(for detail see pthread.py).
                                     If isProxy and proxyConfig:

                                     (1) First you have to pass value of 'type' into the proxyConfig, when type==1, it means you should define a static list with proxys,like :
                                      proxyConfig = {'type':1, 'proxyInfo':[your ips here]},
                                      then programme will choose one every cycle when request randomly;

                                      (2)Some ip supporters support ips with authentic information like "user" and "password" and so on,for exmaple:
                                      proxyConfig = {'type':2, 'proxyInfo':[{'host':'http://www.s_ips.com','port':'3827', 'user':'aa', 'password':'aa'},{'host':'http-dyn.ipclouds.com','port':'2222', 'user':'aa', 'password':'aa'}]}
                                      And type should be 2.
    :param crawlConfig: :            Nowly it only contains maxtime,timeout and encoding,see above
    :param urlConfig:   :            urlConfig includes all the request headers that satisfield your demands.
    :param kwargs:      :
    :return:
    """

    # default headers
    urlConfig_ = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0',
                  'Referer': '',
                  'Host': '',
                  'Cookie': '',
                  'Upgrade-Insecure-Request': 1}

    # default crawl config or settings
    crawlConfig_ = {'timeout': timeout,
                    'encoding': encoding,
                    'maxtime': maxtime}

    proxyConfig_ = {'type': 1, 'isProxy':False, 'proxyInfo':['1','2','3']}

    # bring out protocol of destination url, like 'http' and 'https',to set proxy header if necessary
    protocol = url[:url.find(':')]

    # if urlConfig is not None, continue to update urlConfig_, with urlConfig as standard, else make **kwargs as standard if passed
    if not urlConfig:
        urlConfig_.update(
            {x.replace('_', '-'): kwargs[x] for x in kwargs if 65 <= ord(str(x)[0]) <= 90 and kwargs[x] != ''})

    else:
        urlConfig_.update({x: urlConfig[x] for x in urlConfig if 65 <= ord(str(x)[0]) <= 90 and urlConfig[x] != ''})

    # same to urlConfig
    if not crawlConfig:
        crawlConfig_.update({x: kwargs[x] for x in kwargs if
                             type(kwargs[x]) == str and kwargs[x] is not None and x in ['maxtime', 'tiemout',
                                                                                        'encoding']})
    else:
        crawlConfig_.update({x: kwargs[x] for x in crawlConfig if
                             type(crawlConfig[x]) == str and crawlConfig[x] is not None and x in ['maxtime', 'tiemout',
                                                                                                  'encoding']})

    if proxyConfig:
        proxyConfig_.update(proxyConfig)

    index = 0
    while index <= crawlConfig_['maxtime']:

        try:
            if proxyConfig_['isProxy']:

                if str(proxyConfig['type']) == '1':  # 自定义代理池
                    proxyList = proxyInfo = proxyConfig['proxyInfo']
                    proxy = random.choice(proxyList)
                    proxyData = 'http://' + proxy

                proxyHandler = urllib.request.ProxyHandler({protocol: proxyData})
                opener = urllib.request.build_opener(proxyHandler)

            else:
                opener = urllib.request.build_opener()

            headers = list(zip(list(urlConfig_.keys()), [urlConfig_[x] for x in list(urlConfig_.keys())]))
            opener.addheaders = headers

            try:
                rawHtml = opener.open(url, timeout=crawlConfig_['timeout'])
                if rawHtml.code != 200:
                    assert rawHtml.code == 200, '返回码%s不等于200,url:%s' % (rawHtml.code, url)
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
                log.critical('BadStatusLine Error, URL:%s' % url)
            except urllib.error.URLError as e:
                index += 0.2
                log.critical('URLError, URL:%s, ERROR:%s' % (url, e))
            except Exception as e:
                log.error('Other Error, URL:%s, ERROR:%s' % (url, e))
        except Exception as e:
            log.critical('...', e)

    log.error('Index is over than %s times,crawl fail, URL;%s' % (crawlConfig_['maxtime'], url))
    return None