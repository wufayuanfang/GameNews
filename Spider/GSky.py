import requests
from lxml import etree
from requests.exceptions import RequestException
import datetime
import re
import json
import urllib.parse
import os, django
import time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoNews.settings")
django.setup()
from gnews.models import GNews
from gnews.models import Image_article


def get_page(url):
    try:
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'

        }

        time.sleep(0.2)
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
            # print(response.text)
        else:
            print('没请求到数据')
            return None

    except RequestException:
        print("捕抓到报错了！")
        return None


def get_page_news(jsons, day):
    pattern = re.compile(r'[(](.*)[)]')
    data = json.loads(pattern.findall(jsons)[0])
    html = data.get('body')
    response = etree.HTML(html)

    news_titles = response.xpath('//li/div[@class="img"]/a/@title')
    news_links = response.xpath('//li/div[@class="img"]/a/@href')
    news_covers = response.xpath('//li/div[@class="img"]/a/img/@src')
    news_dates = response.xpath('//li/div[@class="con"]/div[@class="tme"]/div[@class="time"]/text()')
    # print(day)
    for x in zip(news_dates, news_links, news_covers, news_titles):

        news_date = x[0]
        news_link = x[1]
        news_cover = x[2]
        news_title = x[3]
        # 把提取到的时间字符串变为年月日且把时分秒剪掉
        news_date = datetime.datetime.strptime(news_date, '%Y-%m-%d %H:%M').strftime('%Y-%m-%d')
        if news_date == day:
            # print(news_title)
            # print(news_date)
            # print(news_cover)
            # print(news_link)
            # 创造一个列表用来装新闻的页面（每个新闻的页面数量不同）
            url_links = []
            url_links.append(news_link)
            pages = get_pages(get_page(news_link))

            if pages is not None:
                url_links = url_links + pages

            all_contens, video_links, images = get_contens(url_links)
            if video_links is not None:
                video_links = video_links[0]

            new_from = 'https://www.gamersky.com'

            try:
                article = GNews.objects.create(article_title=news_title, article_date=news_date,
                                               article_cover=news_cover,
                                               article_contents=all_contens, article_from=new_from,
                                               article_video=video_links)

                for image in images:
                    Image_article.objects.create(gnews=article, image_title=None, image_links=image)
                print('添加了一条数据')
            except:
                print("添加数据出错了！1.数据库是否在运行？ 2.重复添加数据？")
    if news_date < day:
        return False
    else:
        return True


def get_pages(html):
    if html is not None:
        response = etree.HTML(html)
        pagegs = response.xpath('//div[@class="Mid2L_con"]/span/div/a/@href')[0:-1]

        if pagegs != []:
            return pagegs
        else:
            return None


def get_contens(url_list):
    all_contens = ''
    all_links = []
    all_images = []
    for url in url_list:
        html = get_page(url)

        # 返回的数据是正常的
        if html is not None:
            html = html.encode('ISO-8859-1').decode(requests.utils.get_encodings_from_content(html)[0])
            response = etree.HTML(html)
            news_contens = response.xpath('//div[@class="Mid2L_con"]/p/text()')

            images = response.xpath('//div[@class="Mid2L_con"]/p[@align="center"]/a/@href')
            if images is not []:
                all_images = all_images + images

            # video_links = response.xpath('//div[@class="Mid2L_con"]/p[@align="center"]/script/text()')
            video_links = response.xpath('//div[@class="Mid2L_con"]/p[@align="center"]/script/text()')
            if video_links != []:
                pattern = re.compile(r'"https://v.youku.com/v_show/id_(.*)==.html')
                pattern2 = re.compile(r"src='(.*)==")
                pattern3 = re.compile(r'"http://v.youku.com/v_show/id_(.*)==.html')
                for video_link in video_links:
                    if pattern.findall(video_link) != []:
                        video_link = '//player.youku.com/embed/' + pattern.findall(video_link)[0]
                    elif pattern2.findall(video_link) != []:
                        video_link = pattern2.findall(video_link)[0]
                    elif pattern3.findall(video_link) != []:
                        video_link = '//player.youku.com/embed/' + pattern3.findall(video_link)[0]

                    all_links.append(video_link)

            for news_conten in news_contens:
                news_conten = news_conten.replace('更多相关资讯请关注：', '')
                all_contens = all_contens + news_conten

    if all_links == []:
        all_links = None

    return all_contens, all_links, all_images


if __name__ == '__main__':
    day = (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime('%Y-%m-%d')
    for page in range(1, 6, 1):
        print('第' + str(page) + '页')
        jsondata = '{"type":"updatenodelabel","isCache":true,"cacheTime":60,"nodeId":"20900","isNodeId":"true","page":' + str(
            page) + '}'
        jsondata = urllib.parse.quote(jsondata)
        url = 'https://db2.gamersky.com/LabelJsonpAjax.aspx?callback=jQuery1830898326556654258_1582635998442&jsondata=' + jsondata
        get_page_news(get_page(url), day)


def spider_gsky_begin(day):
    page = 1

    print('开始爬gsky')
    while True:
        print('嗅探页数：' + str(page))
        print('第' + str(page) + '页')
        jsondata = '{"type":"updatenodelabel","isCache":true,"cacheTime":60,"nodeId":"20900","isNodeId":"true","page":' + str(
            page) + '}'
        jsondata = urllib.parse.quote(jsondata)
        url = 'https://db2.gamersky.com/LabelJsonpAjax.aspx?callback=jQuery1830898326556654258_1582635998442&jsondata=' + jsondata
        if get_page_news(get_page(url), day) is not True:
            break
        page += 1

    print('爬gsky结束')
