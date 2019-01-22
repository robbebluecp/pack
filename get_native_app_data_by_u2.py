import urllib.request
import re
import json
import urllib.parse


def get_native_app_data_by_u2(ip, port=7912, app_name='手机淘宝', isPrint=False):
    """
    :param ip:      手机IP
    :param port:    手机端口，默认7912
    :return:        None

    Intention1：
        当前“超级抓包”工具存放截取的数据路径如下：
        1、根路径(root)：http://192.168.0.135:7912/raw/sdcard/vpncapturepro/parsedata/
        2、子路径(sub_root)：2019_01_22_15_32_31_31/%E6%89%8B%E6%9C%BA%E6%B7%98%E5%AE%9D/TCP_203.119.213.109_re_443_lo_58285/sslCaptureData_0.txt
        该function的方法是从root往下一级一级寻找
    Intention2：
        该function建立在uiautomator的

    """

    # 根路径
    root_url = 'http://%s:%s/raw/sdcard/vpncapturepro/parsedata/' % (ip, port)
    try:
        html = urllib.request.urlopen(root_url).read().decode('utf8', errors='ignore')
    except:
        return

    roots = re.findall('">(.*?)</a>', html)
    first_urls = []

    # 00文件为临时存放文件，不保存关键数据
    for i in roots:
        if i.find('_00') > 0:
            continue
        else:
            first_urls.append(root_url + i)
    if not first_urls:
        return

    # 保证每次从最远的数据开始收集,在运行该函数前，尽可能保证之前的数据已经清除
    first_urls.sort()
    second_urls = []
    for first_url in first_urls:
        try:
            # 仅针对淘宝平台进行数据抓取
            html = urllib.request.urlopen(first_url).read().decode('utf8', errors='ignore')
            if html.find(app_name) < 0:
                continue
            else:
                # 中文转码
                second_urls.append(first_url + '%s/' % urllib.parse.quote(app_name))
        except:
            continue
    if not len(second_urls):
        return
    second_urls.sort()
    third_urls = []
    for second_url in second_urls:
        try:
            html = urllib.request.urlopen(second_url).read().decode('utf8', errors='ignore')
        except:
            continue
        file_roots = re.findall('">(.*?)</a>', html)
        file_roots.sort()
        for file_root in file_roots:
            # 这是最终文件的地址
            third_urls.append(second_url + file_root)
    if not third_urls:
        return
    # 组成完整的文件路径
    third_urls = list(map(lambda x: x + 'sslCaptureData_0.txt', third_urls))
    for url in third_urls:
        try:
            try:
                # TODO 完善与临时服务交互方式
                html = urllib.request.urlopen(url).read().decode('utf8', errors='ignore')
            except:
                continue
            if html.find('relationrecommend') > 0 or html.find('appsearch') > 0:
                # 提取重要数据
                items = html[html.find('{'):].strip().replace('\\', '')
                # 整体数据清洗
                items = items.replace('"{', "{").replace('}"', "}")
                # 3C部分数据清洗
                # TODO 补充其余待清洗数据格式
                try:
                    # 品类抓取第一范式
                    items = json.loads(items)
                except:
                    try:
                        # 品类抓取第二范式(3C类)
                        tmp = re.search('"\[([\S\s]+?)",', items).group(1)
                        items.replace('"[%s",' % tmp, "'''%s'''," % tmp)
                        items = json.loads(items)
                    except:
                        # 搜索词抓取第一范式
                        prices = re.findall('"price":"(.*?)"', items)
                        titles = re.findall('"title":"(.*?)",', items)
                        itemids = re.findall('item_id=(\d+)"', items)
                        volume = re.findall('"sold":"(\d+)"', items)
                        data = list(zip(itemids, titles, volume, prices))
                        result = list(map(lambda x: {'itemid': x[0], 'title': x[1], 'volume': x[2], 'price': x[3]}, data))
                        if isPrint:
                            print(result)
                        continue
                data = items['data']['result'][0]['itemsArray']

                result = []
                for item in data:
                    price = item['atmosphere']['price']
                    volume = item['sold']
                    itemid = item['item_id']
                    title = item['title']
                    insert_data = {'price': price, 'title': title, 'itemid': itemid, 'volume': volume, 'location': url}
                    result.append(insert_data)
                if isPrint:
                    print(result)
            # TODO 加入ADB清除缓存功能
        except Exception as e:
            print(e)

get_native_app_data_by_u2('192.168.0.135', isPrint=True)