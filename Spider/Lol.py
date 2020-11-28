import datetime
import os
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

import django
import re
import requests
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GameNews.settings")
django.setup()

from gnews.models import Video


def getpage(url):
    req = Request(url)
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                 'Chrome/79.0.3945.130 Safari/537.36 '
    req.add_header('User-Agent', user_agent)
    try:
        response = urlopen(url)
    except HTTPError as e:
        print('The server couldnt fulfill the request.')
        print('Error code:', e.code)
    except URLError as e:
        print('We failed to reach a server.')
        print('Reason:', e.reason)
    html = response.read().decode('utf-8')
    return (html)


def getvideo(web):
    if re.search(r'vid=', web):
        patten = re.compile(r'vid=(.*)')
        vid = patten.findall(web)
        vid = vid[0]
    else:
        newurl = (web.split("/")[-1])
        vid = newurl.replace('.html', ' ')
    # 从视频页面找出vid
    # vid = 'p30716ikruo'  # replace with your vid
    vid = vid.replace(' ', '')
    params = {
        'isHLS': False,
        'charge': 0,
        'vid': vid,
        'defn': 'shd',
        'defnpayver': 1,
        'otype': 'json',
        'platform': 10901,
        'sdtfrom': 'v1010',
        'host': 'v.qq.com',
        'fhdswitch': 0,
        'show1080p': 1,
    }
    r = requests.get('http://h5vv.video.qq.com/getinfo', params=params)
    data = json.loads((r.content[len('QZOutputJson='):-1]).decode('utf-8'))
    # try:
    #     url_prefix = data['vl']['vi'][0]['ul']['ui'][0]['url']
    # except:
    url_prefix = 'http://ugcyd.qq.com/uwMROfz2r5zBIaQXGdGnC2dfJ6nAzEoO290Tsw9-2jpi_xWl'

    # if len(url_prefix) == 139:
    #     url_prefix = 'http://ugcyd.qq.com/uwMROfz2r5zBIaQXGdGnC2dfJ6nAzEoO290Tsw9-2jpi_xWl'

    urls = []
    try:
        for stream in data['fl']['fi']:
            if stream['name'] != 'shd':
                continue
            stream_id = stream['id']
            urls = []
            try:
                for d in data['vl']['vi'][0]['cl']['ci']:
                    keyid = d['keyid']
                    filename = keyid.replace('.10', '.p', 1) + '.mp4'
                    params = {
                        'otype': 'json',
                        'vid': vid,
                        'format': stream_id,
                        'filename': filename,
                        'platform': 10901,
                        'vt': 217,
                        'charge': 0,
                    }
                    r = requests.get('http://h5vv.video.qq.com/getkey', params=params)
                    data = json.loads((r.content[len('QZOutputJson='):-1]).decode('utf-8'))
                    url = '%s/%s?sdtfrom=v1010&vkey=%s' % (url_prefix, filename, data['key'])
                    # print(url_prefix)
                    # print(url1)
                    urls.append(url)
            except:
                pass
    except:
        pass
    # print('stream:', stream['name'])
    # for url in urls:
    #     print(url)
    if len(urls) < 1:
        return None
    return urls[0]


if __name__ == '__main__':
    url = 'https://apps.game.qq.com/wmp/v3.1/?p0=3&p1=searchKeywordsList&page=1&pagesize=20&order=sIdxTime&type=&id=&r0=jsonp&source=web_pc'

    html = getpage(url)
    url_r = re.compile(r'"sUrl":"(.*?)"')
    title_r = re.compile(r'"sTitle":"(.*?)"')
    time_r = re.compile(r'"sIdxTime":"(.*?)"')
    vid = url_r.findall(html)
    title = title_r.findall(html)
    time = time_r.findall(html)
    today = (datetime.datetime.now() + datetime.timedelta(days=-0)).strftime('%Y-%m-%d')
    for v in zip(vid, title, time):
        if len(v[0]) > 0:
            date = datetime.datetime.strptime(v[2], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
            print(date, today)
            if date < today:  # 到达指定日期之前不往下走了
                break
            if date == today:
                url_video = getvideo(v[0])
                print(url_video)
                if url_video is not None:
                    try:
                        # Video.objects.create(video_title=v[1], video_date=date, video_link=url_video)
                        print('添加了一条数据')
                    except:
                        print('防止重复添加')


def spider_lol_begin(day):
    video_from = 'lol'
    page = 1
    print('开始爬LOL视频')
    while True:
        print('第' + str(page) + '页')
        url = 'https://apps.game.qq.com/wmp/v3.1/?p0=3&p1=searchKeywordsList&page=' + str(
            page) + '&pagesize=28&order=sIdxTime&type=&id=&r0=jsonp&source=web_pc'
        html = getpage(url)
        url_r = re.compile(r'"sUrl":"(.*?)"')
        title_r = re.compile(r'"sTitle":"(.*?)"')
        time_r = re.compile(r'"sIdxTime":"(.*?)"')
        vid = url_r.findall(html)
        title = title_r.findall(html)
        time = time_r.findall(html)
        for v in zip(vid, title, time):
            if len(v[0]) > 0:
                date = datetime.datetime.strptime(v[2], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
                # print(date, today)
                if date < day:  # 到达指定日期之前不往下走了
                    print('爬LOL视频结束')
                    return
                if date == day:
                    url_video = getvideo(v[0])
                    # print(url_video)
                    if url_video is not None:
                        try:
                            Video.objects.create(video_title=v[1], video_date=date, video_from=video_from,
                                                 video_link=url_video)
                            print('添加了一条数据')
                        except:
                            print('防止重复添加')
        page += 1
