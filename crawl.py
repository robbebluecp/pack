import urllib.request
import random
import urllib.parse


def crawl(url, **kwargs):

    """

    This package includes one function for url decoding.

    :param url          :           url
    :param kwargs       :           params for request or response or decoding

    By default, we support some params for you to use, but if you want to change, just deliver what you want
    to use with param kwargs.

    For example:
        crawl(url, timeout=5, maxtime=10, isProxy=True, proxyMode=1)

        Explanation: this example means that the max wait time per request is 5 second,
                     times for another request when request failed is 10,
                     and we choose to use proxy to request for response with proxyMode 1.

    :param timeout       :          wait time for request
    :param maxtime       :          max time for trial to request
    :param encoding      :          decode way for decoing html
    :param isProxy       :          whether or not choose to use proxy
    :param proxyMode     :          if we choose to use proxy, proxyMode must be deliver

    And some other params we won't describe detaily

    """

    crawlConfig = {'maxtime': 5, 'timeout': 10, 'isProxy': False, 'encoding': 'utf8'}
    crawlConfig.update(kwargs)

    urlConfig = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0',
                 'Referer': '',
                 'Cookie': ''}

    urlConfig.update({x: kwargs[x] for x in kwargs if 65 <= ord(str(x)[0]) <= 90 and kwargs[x] != ''})

    headerList = list(sorted(urlConfig.items(), key=lambda x: x[0]))

    urlProtocal = url[:url.find(":")]

    try:
        if crawlConfig['isProxy']:
            try:
                if crawlConfig['proxyMode'] == 1:
                    proxyList = crawlConfig['urlRemarks']['proxyContent']
                    proxyIndex = random.randrange(len(proxyList))
                    proxyUser = proxyList[proxyIndex][0]
                    proxyPassword = proxyList[proxyIndex][1]
                    proxyHost = crawlConfig['proxyHost']
                    proxyPort = crawlConfig['proxyPort']
                    proxyData = """%(urlProtocal)s://%(proxyUser)s:%(proxyPassword)s@%(proxyHost)s:%(proxyPort)s""" % {
                        'urlProtocal': urlProtocal,
                        'proxyUser': proxyUser,
                        'proxyPassword': proxyPassword,
                        'proxyHost': proxyHost,
                        'proxyPort': proxyPort
                    }
                    proxyOperation = urllib.request.ProxyHandler({'%s' % urlProtocal: '%s' % proxyData})
                    opener = urllib.request.build_opener(proxyOperation)
                if crawlConfig['proxyMode'] == 2:
                    requestRawInfo = {}
                    for info in headerList:
                        requestRawInfo[info[0]] = info[1]
                    requestRawInfo['url'] = url
                    requestDecodeInfo = urllib.parse.urlencode(requestRawInfo)
                    url = 'http://proxy.venndata.cn/crawl?' + requestDecodeInfo
                    opener = urllib.request.build_opener()
            except:
                opener = urllib.request.build_opener()
        else:
            opener = urllib.request.build_opener()

    except:
        opener = urllib.request.build_opener()
    opener.addheaders = headerList
    try:
        maxtime = crawlConfig['maxtime']
    except:
        maxtime = 5
    while maxtime > 0:
        try:
            rawHtml = opener.open(url, timeout=crawlConfig['timeout'])
            if rawHtml.code != 200:
                maxtime -= 1
                html = None
            else:
                try:
                    html = rawHtml.read().decode(crawlConfig['encoding'], errors='ignore')
                    return html
                except Exception as e:
                    maxtime -= 1
                    html = None
        except Exception as e:
            print(e)
            maxtime -= 1
            html = None

    return html
