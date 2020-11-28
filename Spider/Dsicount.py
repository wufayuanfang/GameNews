import requests
from lxml import etree
from requests.exceptions import RequestException
import os, django
import time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GameNews.settings")
django.setup()
from index.models import Discount


def get_page(url):
    try:
        headers = {
            'User - Agent': 'Mozilla / 5.0(Windows NT 10.0;Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
            'Accept - Language': 'zh - CN, zh;q = 0.9'
        }
        time.sleep(0.1)
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
            # print(response.text)
        return None

    except RequestException:
        print("捕抓到报错了！")
        return None


def get_page_num(html):
    response = etree.HTML(html)
    num = response.xpath('//div[@class="pagination-container"]/ul/li/a/text()')[-2]
    return int(num)


def get_discount(html, type):
    response = etree.HTML(html)
    imaUrls = response.xpath('//ul[@class="u_stylelessList"]/li/a/img/@src')
    names = response.xpath('//ul[@class="u_stylelessList"]/li/a/div/div[1]/p[1]/text()')
    discounts = response.xpath('//ul[@class="u_stylelessList"]/li/a[@class="gameInfo"]/div/div[1]/p[2]/span[1]/text()')
    currents = response.xpath('//ul[@class="u_stylelessList"]/li/a[@class="gameInfo"]/div/div[2]/p[1]/text()')
    states = response.xpath('//ul[@class="u_stylelessList"]/li/a[@class="gameInfo"]/div/div[2]/p[2]/text()')
    originals = response.xpath('//ul[@class="u_stylelessList"]/li/a[@class="gameInfo"]/div/div[2]/p[2]/span/text()')

    for dis in zip(imaUrls, names, discounts, currents, states, originals):
        d = Discount(imageUrl=dis[0], name=dis[1], dis=dis[2], current=dis[3], state=dis[4], original=dis[5],
                     type=type)
        d.save()
        print('添加了1条数据')


def get_platform(platform, type):
    Discount.objects.filter(type=type).delete()  # 清空旧数据
    url_begin = 'https://www.gcores.com/games/discount?platform=' + platform + '&chinese=false&page=1&sort=onsale-start'
    pages = get_page_num(get_page(url_begin))
    for page in range(1, pages + 1):
        url = 'https://www.gcores.com/games/discount?platform=' + platform + '&chinese=false&page=' + str(
            page) + '&sort=onsale-start'
        get_discount(get_page(url), type)
    print(type + '部分爬取完成')


def get_all_discount():
    platform = ['all', 'Steam', 'Nintendo%20Switch', 'PlayStation%204', 'Xbox%20One']
    type = ['All', 'Steam', 'Switch', 'PS4', 'Xbox']
    for x in zip(platform, type):
        get_platform(x[0], x[1])
    print('游戏折扣数据全部爬取完成')


if __name__ == '__main__':
    get_all_discount()
