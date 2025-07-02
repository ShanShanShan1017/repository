import random
import time

import requests
import threading
import pandas as pd
from lxml import etree
import openpyxl
# 全部信息列表
count = list()

# 代理IP列表，需要自行收集或购买有效代理
proxy_list = [
    '202.101.213.147',
    '39.107.250.25',
    # 更多代理IP
]
# User - Agent列表
user_agent_list = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36',
    'Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36'
     # Opera
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60",
    "Opera/8.0 (Windows NT 5.1; U; en)",
    "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50",

    # Firefox
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",

    # Safari
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",

    # chrome
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",

    # 360
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",


    # 淘宝浏览器
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",

    #猎豹浏览器
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)" ,

    # QQ浏览器
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E) ",

    # sogou浏览器
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)",

    # maxthon浏览器
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36",

    # UC浏览器
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36",

    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36",

    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X; zh-CN) AppleWebKit/537.51.1 (KHTML, like Gecko) Mobile/17D50 UCBrowser/12.8.2.1268 Mobile AliApp(TUnionSDK/0.1.20.3)",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36",

    "Mozilla/5.0 (Linux; Android 8.1.0; OPPO R11t Build/OPM1.171019.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.19 SP-engine/2.15.0 baiduboxapp/11.19.5.10 (Baidu; P1 8.1.0)",

    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",

    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 SP-engine/2.14.0 main%2F1.0 baiduboxapp/11.18.0.16 (Baidu; P2 13.3.1) NABar/0.0 ",

    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134",

    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",

    "Mozilla/5.0 (iPhone; CPU iPhone OS 12_4_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.10(0x17000a21) NetType/4G Language/zh_CN",

    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",

    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",

    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",

    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36",

    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",

]



# 生成1-10页url
def url_creat():
    # 基础url
    url = 'https://zz.lianjia.com/ershoufang/erqiqu/pg{}/'
    # 生成前10页url列表
    links = [url.format(i) for i in range(1,100)]
    return links


# 对url进行解析
def url_parse(url):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'SECKEY_ABVK=FYV7EHcL9lweiD79T9QWRvdhNGPql2QOZdlsa3+zE8eXbcSSyZEfzVhoBhuPxok1sfXCQMQuW3PPbU1jYBIxbg%3D%3D; BMAP_SECKEY=FYV7EHcL9lweiD79T9QWRvdhNGPql2QOZdlsa3-zE8fmrkwz06hQJKZOOzsV-HnY7c6ZcLNFIHxSNzC2a0oGwuODjLrQTOOIZFbrRcjwS7CG6a4f8L6BdEf0ypUJiOS_pzUHUYfjsgOba5bmOlDmjC0RJn-jBlkqHN6BxQkqpTfk6MRMwkM5itPs4hcyQNnA6Au-uw5pH0xXFsi5l5npXw; lianjia_uuid=f17a81c9-41aa-42a8-ba5e-f122073afd04; _ga=GA1.2.1825377094.1745911240; crosSdkDT2019DeviceId=zeaohb--vj7gdi-b5m441g2i3nhr4p-qw7qqckn8; login_ucid=2000000480436410; lianjia_token=2.0015180c6d4021813b04b5255c609cd62c; lianjia_token_secure=2.0015180c6d4021813b04b5255c609cd62c; security_ticket=Rt3m7Ebjfe91MPuo/rpP8k2YVxdcxMyZINcT1bAiPrPr5UQnkB+wdYb7eC18vOJpp0HDXr7u6DLpd0gkrJxJBF2+zxZZJq6yV5yVbEVNsjaRomm5FPW97W9BS2c25yQmiCEe/Z3H7yJR+jk8iQ/Ul2JoLyfR2mrbjLvJyOyP0LU=; ftkrc_=76076a57-7a95-4b6d-921a-bf9899981d50; lfrc_=0ffddd61-d80f-4df5-8724-416f81901a9a; _jzqa=1.4351281326758447600.1745911229.1746269370.1746273328.7; _jzqx=1.1745911229.1746273328.5.jzqsr=cn%2Ebing%2Ecom|jzqct=/.jzqsr=zz%2Elianjia%2Ecom|jzqct=/ershoufang/; _qzja=1.221223150.1745911228997.1746269369592.1746273328423.1746270916602.1746273328423.0.0.0.18.7; select_city=410100; lianjia_ssid=e6e21447-33e7-484b-97bf-f35b43098f3a; Hm_lvt_46bf127ac9b856df503ec2dbf942b67e=1745911229,1746512087; HMACCOUNT=FC1847C9F9B3D481; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22196806b2b5581d-0a4c9b4d5be24e-4c657b58-1024000-196806b2b56d05%22%2C%22%24device_id%22%3A%22196806b2b5581d-0a4c9b4d5be24e-4c657b58-1024000-196806b2b56d05%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.bing.com%2F%22%2C%22%24latest_referrer_host%22%3A%22www.bing.com%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_utm_source%22%3A%22biying%22%2C%22%24latest_utm_medium%22%3A%22pinzhuan%22%2C%22%24latest_utm_campaign%22%3A%22wybeijing%22%2C%22%24latest_utm_content%22%3A%22biaotimiaoshu%22%2C%22%24latest_utm_term%22%3A%22biaoti%22%7D%7D; _gid=GA1.2.732432111.1746512089; Hm_lpvt_46bf127ac9b856df503ec2dbf942b67e=1746512975; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiNjE1ZjgzOGQzMjRhYjA5YjZiZDhjNjhjNjEwMjI5MjNhYjE1NzM1NDFjYzhlZTkzMjA2NDViZGM3NmEwMTkyODQyYTM1NzNjYzNhMTFkMzc4OTdmMjJhNTAyYzFmNjcxYzczYzc2ODQ0YTMxODlmYWExYzIxMTJhYzc1ZmY3MzAwNjhhYTM1MjZmMjVjZjU4NmRiN2Q5NThmMzMzMmU1NmQyNWZhMzNmNDIzNWZlOTkzMWFhYjlmNDQ4ZTNhY2EyMTgyYzFmNDI0MWI2Yjc5YTFhZTFjMjM0NTFlNTBmN2RlMGE0MmJjYzU5MmRhOTdiMjZkMWFjYzE1ZWY3ODEzNVwiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCJhOWZlMjQyZlwifSIsInIiOiJodHRwczovL3p6LmxpYW5qaWEuY29tL2Vyc2hvdWZhbmcvZXJxaXF1L3BnMi8iLCJvcyI6IndlYiIsInYiOiIwLjEifQ==',
        'Host': 'zz.lianjia.com',
        'Pragma': 'no-cache',
        'Referer': 'https://zz.lianjia.com/ershoufang/erqiqu/',
        'sec-ch-ua': '"Chromium";v="136", "Microsoft Edge";v="136", "Not.A/Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform':'"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': random.choice(user_agent_list)}
    try:
        response = requests.get(url=url, headers=headers,allow_redirects=False)
        # 处理响应
        if response.status_code in [301, 302]:  # 重定向状态码
            new_url = response.headers.get('Location')
            print(f"遇到重定向，新的 URL 是: {new_url}")
        else:
            print(response.text)
    except requests.RequestException as e:
        print(f"请求发生错误: {e}")

    tree = etree.HTML(response.text)
    # ul列表下的全部li标签
    li_List = tree.xpath("//*[@class='sellListContent']/li")
    # 创建线程锁对象
    lock = threading.RLock()
    # 上锁
    lock.acquire()
    for li in li_List:
        # 标题
        title = li.xpath('./div/div/a/text()')[0]
        # # 图片
        # img = li.xpath('./a/img[2]/@src')[0]
        # 网址
        link = li.xpath('./div/div/a/@href')[0]
        # 位置
        postion = li.xpath('./div/div[2]/div/a/text()')[0] + li.xpath('./div/div[2]/div/a[2]/text()')[0]
        # 类型
        types = li.xpath('./div/div[3]/div/text()')[0].split(' | ')[0]
        # 面积
        area = li.xpath('./div/div[3]/div/text()')[0].split(' | ')[1]
        # 房屋信息
        info = li.xpath('./div/div[3]/div/text()')[0].split(' | ')[2:-1]
        info = ''.join(info)
        # 总价
        count_price = li.xpath('.//div/div[6]/div/span/text()')[0] + '万'
        # 单价
        angle_price = li.xpath('.//div/div[6]/div[2]/span/text()')[0]
        dic = {'标题': title, "位置": postion, '房屋类型': types, '面积': area, "单价": angle_price,
               '总价': count_price, '介绍': info, "网址": link}
        print(dic)
        # 将房屋信息加入总列表中
        count.append(dic)
    # 解锁
    lock.release()


def run():
    links = url_creat()
    # 多线程爬取
    for i, url in enumerate(links):
        x = threading.Thread(target=url_parse, args=(url,))
        x.start()
        # 控制请求频率，每隔1 - 3秒发送一次请求
        time.sleep(random.uniform(1, 3))
    # 等待所有线程完成
    for x in threading.enumerate():
        if x != threading.current_thread():
            x.join()
    # 将全部房屋信息转化为excel
    data = pd.DataFrame(count)
    with pd.ExcelWriter('房屋信息.xlsx', engine='openpyxl') as writer:
        data.to_excel(writer, index=False)


if __name__ == '__main__':
    run()
