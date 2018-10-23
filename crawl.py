import urllib.request
import random
try:
    import log
except:
    from . import log
try:
    import useragents
except:
    from . import useragent
try:
    from parseconfig import Parse
except:
    from .parseconfig import Parse
import gzip
import http.client
import urllib.error
import urllib.parse





class Crawl:

    def __init__(self, url, timeout=5, encoding='utf8', maxtime=5, data=None, isProxy=False, proxyPools=None, crawlConfig=None, urlConfig=None,  **kwargs):
        self.url = url
        self.timeout = timeout
        self.maxtime = maxtime
        self.encoding = encoding
        self.data = data
        self.isProxy = isProxy
        self.proxyPools = proxyPools
        self.crawlConfig = crawlConfig
        self.urlConfig = urlConfig

        self.protocol = url[:url.find(':')]
        self.kwargs = kwargs

        self.html = None

        self.parse_config()
        self.run()

    def parse_config(self):
        urlConfig_ = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0',
                      'Referer': '',
                      'Host': '',
                      'Cookie': ''}

        crawlConfig_ = {'timeout': self.timeout,
                        'encoding': self.encoding,
                        'maxtime': self.maxtime}

        if not self.urlConfig:
            urlConfig_.update(
                {x.replace('_', '-'): self.kwargs[x] for x in self.kwargs if 65 <= ord(str(x)[0]) <= 90 and self.kwargs[x]})

        else:
            urlConfig_.update({x: self.urlConfig[x] for x in self.urlConfig if 65 <= ord(str(x)[0]) <= 90 and self.urlConfig[x]})

        if not self.crawlConfig:
            crawlConfig_.update({x: self.kwargs[x] for x in self.kwargs if
                                 type(x) == str and self.kwargs[x] is not None and x in ['maxtime', 'timeout',
                                                                                            'encoding']})
        else:
            crawlConfig_.update({x: self.kwargs[x] for x in self.crawlConfig if
                                 type(x) == str and self.crawlConfig[x] is not None and x in ['maxtime', 'timeout',
                                                                                                  'encoding']})
        if self.proxyPools:
            self.isProxy = True

        self.urlConfig, self.crawlConfig = urlConfig_, crawlConfig_

    def opener(self):
        if self.isProxy and self.proxyPools:
            proxy = random.choice(self.proxyPools)
            proxyData = 'http://' + proxy
            proxyHandler = urllib.request.ProxyHandler({self.protocol: proxyData})
            opener = urllib.request.build_opener(proxyHandler)
        else:
            opener = urllib.request.build_opener()
        if Parse.crawlConfig['shuffle']:
            self.urlConfig['User-Agent'] = random.choice(useragents.userAgents)
        headers = list(zip(list(self.urlConfig.keys()), [self.urlConfig[x] for x in list(self.urlConfig.keys())]))
        opener.addheaders = headers
        return opener

    def run(self):
        index = 0
        while index <= self.crawlConfig['maxtime']:

            try:
                opener = self.opener()
                try:
                    if not self.data:
                        rawHtml = opener.open(self.url, timeout=self.crawlConfig['timeout'])
                    else:
                        data = urllib.parse.urlencode(self.data).encode('utf8')
                        rawHtml = opener.open(self.url, timeout=self.crawlConfig['timeout'], data=data)
                    opener.close()
                    if rawHtml.code != 200:
                        assert rawHtml.code == 200, '返回码%s不等于200,url:%s' % (rawHtml.code, self.url)
                    else:
                        bytes = rawHtml.read()
                        try:
                            data = gzip.decompress(bytes)
                        except:
                            data = bytes
                        self.html = data.decode(self.crawlConfig['encoding'], errors='ignore')
                        return
                except http.client.BadStatusLine:
                    index += 1
                    log.error('BadStatusLine Error, URL:%s' % self.url)
                except urllib.error.URLError as e:
                    index += 0.2
                    log.error('URLError, URL:%s, ERROR:%s' % (self.url, e))
                except Exception as e:
                    log.error('Other Error, URL:%s, ERROR:%s' % (self.url, e))
            except Exception as e:
                log.critical('...', e)

        log.critical('Index is over than %s times,crawl fail, URL;%s' % (self.crawlConfig['maxtime'], self.url))
        self.html = None
