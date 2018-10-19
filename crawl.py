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
import urllib.parse



def crawl(url, timeout=5, encoding='utf8', maxtime=5, data=None, isProxy=False, proxyPools=None, crawlConfig=None, urlConfig=None,
          **kwargs):

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


    # bring out protocol of destination url, like 'http' and 'https',to set proxy header if necessary
    protocol = url[:url.find(':')]

    # if urlConfig is not None, continue to update urlConfig_, with urlConfig as standard, else make **kwargs as standard if passed
    if not urlConfig:
        urlConfig_.update(
            {x.replace('_', '-'): kwargs[x] for x in kwargs if 65 <= ord(str(x)[0]) <= 90 and kwargs[x]})

    else:
        urlConfig_.update({x: urlConfig[x] for x in urlConfig if 65 <= ord(str(x)[0]) <= 90 and urlConfig[x]})

    # same to urlConfig
    if not crawlConfig:
        crawlConfig_.update({x: kwargs[x] for x in kwargs if
                             type(kwargs[x]) == str and kwargs[x] is not None and x in ['maxtime', 'timeout',
                                                                                        'encoding']})
    else:
        crawlConfig_.update({x: kwargs[x] for x in crawlConfig if
                             type(crawlConfig[x]) == str and crawlConfig[x] is not None and x in ['maxtime', 'timeout',
                                                                                                  'encoding']})


    index = 0
    while index <= crawlConfig_['maxtime']:

        try:
            if isProxy:

                proxy = random.choice(proxyPools)
                proxyData = 'http://' + proxy
                proxyHandler = urllib.request.ProxyHandler({protocol: proxyData})
                opener = urllib.request.build_opener(proxyHandler)

            else:
                opener = urllib.request.build_opener()

            headers = list(zip(list(urlConfig_.keys()), [urlConfig_[x] for x in list(urlConfig_.keys())]))
            opener.addheaders = headers

            try:
                if not data:
                    rawHtml = opener.open(url, timeout=crawlConfig_['timeout'])
                else:
                    data = urllib.parse.urlencode(data).encode('utf8')
                    rawHtml = opener.open(url, timeout=crawlConfig_['timeout'], data=data)
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
