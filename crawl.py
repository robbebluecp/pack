import urllib.request
import requests
import random
import json
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

    def __init__(self, url, timeout=5, encoding='utf8', maxtime=5, data=None, isProxy=False, proxyPools=None, crawlConfig=None, urlConfig=None, dateType='str', **kwargs):
        self.url = url
        self.timeout = timeout
        self.maxtime = maxtime
        self.encoding = encoding
        self.data = data
        self.dataType = dateType
        self.isProxy = isProxy
        self.proxyPools = proxyPools
        self.crawlConfig = crawlConfig
        self.urlConfig = urlConfig

        self.protocol = url[:url.find(':')]
        self.kwargs = kwargs

        self.html = None

        self.parse_config()
        self.run()

    def get_proxy(self):
        if self.proxyPools:
            self.isProxy = True
            self.proxyData = {self.protocol: 'http://' + random.choice(self.proxyPools)}
        else:
            self.proxyData = {}
        return self.proxyData

    def parse_config(self):
        urlConfig_ = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'}

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
                                 type(x) == str and self.kwargs[x] is not None and x in ['maxtime', 'timeout','encoding']})
        else:
            crawlConfig_.update({x: self.kwargs[x] for x in self.crawlConfig if
                                 type(x) == str and self.crawlConfig[x] is not None and x in ['maxtime', 'timeout','encoding']})

        self.urlConfig, self.crawlConfig = urlConfig_, crawlConfig_

        if Parse.crawlConfig['shuffle']:
            self.urlConfig['User-Agent'] = random.choice(useragents.userAgents)

    def run(self):
        index = 0
        while index <= self.crawlConfig['maxtime']:
            try:
                try:
                    if not self.data:
                        req = requests.get(url=self.url, headers=self.urlConfig, proxies=self.get_proxy(), timeout=self.crawlConfig['timeout'])
                    else:
                        if self.dataType == 'str':
                            data = json.dumps(self.data)
                        else:
                            data = self.data
                        req = requests.post(url=self.url, headers=self.urlConfig, proxies=self.get_proxy(), timeout=self.crawlConfig['timeout'], data=data)
                    if req.status_code != 200:
                        raise Exception('status code is not 200 ! ')
                    self.html = req.content.decode(self.crawlConfig['encoding'], errors='ignore')
                    return self.html


                except (http.client.BadStatusLine, requests.exceptions.ConnectionError) as e:
                    index += 1
                    log.error('BadStatusLine Error, URL:%s' % self.url)

                except urllib.error.URLError as e:
                    index += 0.2
                    log.error('URLError, URL:%s, ERROR:%s' % (self.url, str(e)))

                except Exception as e:
                    index += 1
                    log.error('Other Error, URL:%s, ERROR:%s' % (self.url, str(e)))
            except Exception as e:
                index += 1
                log.critical('...' + str(e))
        log.critical('Index is over than %s times,crawl fail, URL;%s' % (self.crawlConfig['maxtime'], self.url))
        self.html = None


crawl = Crawl
