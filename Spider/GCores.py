import requests
from lxml import etree
from requests.exceptions import RequestException
import datetime
import re
import os, django
import time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoNews.settings")
django.setup()
from gnews.models import GNews


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


def get_page_news(html, day):
    response = etree.HTML(html)

    # 拿到一个页面中的所有新闻的标题标题
    news_titles = response.xpath(
        '//div[@class="col-xl-3 col-md-4 col-sm-6"]/div/div[@class="am_card_inner"]/a/h3/text()')
    # print(news_titles)
    # for news_title in news_titles:
    #     print(news_title)

    # 拿到一个页面中的所有封面链接
    news_covers = response.xpath(
        '//div[@class="col-xl-3 col-md-4 col-sm-6"]/div/div[@class="original_imgArea"]/@style')
    pattern = re.compile(r'[(](.*?)[)]')
    # for news_cover in news_covers:
    #     news_cover = pattern.findall(news_cover)
    #     print(news_cover)

    # 拿到一个页面中的所有链接
    news_links = response.xpath(
        '//div[@class="col-xl-3 col-md-4 col-sm-6"]/div/div[@class="original_imgArea"]/a/@href')
    header = 'https://www.gcores.com'
    # print(news_links)
    # for news_link in news_links:
    #     news_link = header + news_link  # 把链接的头部补上
    #     print(news_link)

    # 拿到新闻的发布时间
    news_dates = response.xpath(
        '//div[@class="col-xl-3 col-md-4 col-sm-6"]/div/div[@class="am_card_inner"]/div[@class="d-flex align-items-end justify-content-between am_card_btm"]/a/div/div/text()')

    # day = (datetime.datetime.now() + datetime.timedelta(days=-0)).strftime('%Y-%m-%d')
    # for news_date in news_dates:  # 把今天的时间转换成统一的日期
    #     if len(news_date) >= 5 and len(news_date) <= 7:
    #         news_date = datetime.datetime.now().strftime('%Y-%m-%d')
    #         # print(news_date)
    #
    #     if len(news_date) == 4:  # 把昨天的日期转换成统一的日期
    #         news_date = (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime('%Y-%m-%d')
    # print(news_date)

    # print([x for x in zip(news_dates, news_links, news_covers, news_titles)])
    for x in zip(news_dates, news_links, news_covers, news_titles):

        news_date = x[0]
        news_link = x[1]
        news_cover = x[2]
        news_title = x[3]
        if len(news_date) >= 5 and len(news_date) <= 7:  # 今天的时间
            news_date = datetime.datetime.now().strftime('%Y-%m-%d')
            # print(news_date)

        if len(news_date) == 4:  # 把昨天的日期转换成统一的日期
            news_date = (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime('%Y-%m-%d')

        if news_date == day:
            # print(news_title)
            # print(news_date)
            news_cover = pattern.findall(news_cover)
            # print(news_cover[0])

            news_link = header + news_link  # 把链接的头部补上
            # print(news_link)
            contens, video_link = get_contens(news_link)

            # print(contens)
            # print(video_link)

            new_from = 'https://www.gcores.com'
            try:
                GNews.objects.create(article_title=news_title, article_date=news_date, article_cover=news_cover[0],
                                     article_contents=contens, article_from=new_from, article_video=video_link)
                print('向数据库添加了1条数据！')
            except:
                print('添加数据出错，可用来防止重复爬取')
                # return False

    if news_date < day:
        return False
    else:
        return True


def get_contens(url):
    html = get_page(url)
    response = etree.HTML(html)

    news_contens = response.xpath(
        '//div[@class="DraftEditor-editorContainer"]/div/div/div[@class="story_block story_block-text "]/div/span/span/text()')

    contens = ''
    for news_conten in news_contens:
        contens = contens + news_conten + '\n'

    video_link = response.xpath(
        '//div[@class="DraftEditor-editorContainer"]/div/div/figure[@class="story_block story_block-atomic story_block-atomic-embed"]/div/div/div/iframe/@src')

    # print(contens)

    if video_link != []:
        video_link = video_link[0]
    else:
        video_link = None

    return contens, video_link


if __name__ == '__main__':
    day = (datetime.datetime.now() + datetime.timedelta(days=-0)).strftime('%Y-%m-%d')
    for page in range(1, 10, 1):
        url = 'https://www.gcores.com/news?page={}'.format(page)
        get_page_news(get_page(url), day)


def spider_gcores_begin(day):
    today = datetime.datetime.now()
    dt = datetime.datetime.strptime(day, "%Y-%m-%d")
    page = int((today - dt).days / 2) + 1

    print('开始爬gcores')
    while True:
        print('嗅探页数：' + str(page))
        url = 'https://www.gcores.com/news?page={}'.format(page)
        if get_page_news(get_page(url), day) is not True:
            break
        page += 1

    print('爬gcores结束')
