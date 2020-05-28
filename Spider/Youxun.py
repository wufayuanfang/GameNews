import requests
from requests.exceptions import RequestException
import datetime
import json
import os, django
import time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoNews.settings")
django.setup()
from gnews.models import GNews


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


def begin_page():
    previd_max = 999999
    url = 'http://dy.www.yxdown.com/news/indexmore.json?callback=viewMoreCallback&previd=' + str(previd_max)
    data = json.loads(get_page(url)[len('viewMoreCallback('):-1])
    previd = data.get('data')[0].get('ArticleID') + 1
    return previd


if __name__ == '__main__':

    news_from = 'http://www.yxdown.com'
    previd = begin_page()

    today = (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime('%Y-%m-%d')

    while True:
        url = 'http://dy.www.yxdown.com/news/indexmore.json?callback=viewMoreCallback&previd=' + str(previd)
        datas = json.loads(get_page(url)[len('viewMoreCallback('):-1])

        for data in datas.get('data'):
            title = data.get('title')
            time_unix = int(data.get('adddate')[len('/Date('):-2]) / 1000
            date = time.strftime("%Y-%m-%d", time.localtime(time_unix))
            cover = data.get('image500')
            content = data.get('content')
            print(date, today)
            if date < today:  # 到达指定日期之前不往下走了
                print('爬虫结束!')
                # return
                break
            if date == today:
                try:
                    GNews.objects.create(article_title=title, article_date=date, article_cover=cover,
                                         article_contents=content, article_from=news_from, article_video=None)
                    print('添加了一条数据')
                except:
                    print('添加错误，防止重复添加')
        previd -= 19  # 翻页


def spider_youxun_begin(day):
    news_from = 'http://www.yxdown.com'
    previd = begin_page()

    while True:
        url = 'http://dy.www.yxdown.com/news/indexmore.json?callback=viewMoreCallback&previd=' + str(previd)
        datas = json.loads(get_page(url)[len('viewMoreCallback('):-1])

        for data in datas.get('data'):
            title = data.get('title')
            time_unix = int(data.get('adddate')[len('/Date('):-2]) / 1000
            date = time.strftime("%Y-%m-%d", time.localtime(time_unix))
            cover = data.get('image500')
            content = data.get('content')
            print(date, today)
            if date < day:  # 到达指定日期之前不往下走了
                print('选定日期过了，爬虫结束!')
                return
            if date == day:
                try:
                    GNews.objects.create(article_title=title, article_date=date, article_cover=cover,
                                         article_contents=content, article_from=news_from, article_video=None)
                    print('添加了一条数据')
                except:
                    print('添加错误，防止重复添加')
        previd -= 19  # 翻页
