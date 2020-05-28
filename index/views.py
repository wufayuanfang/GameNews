# Create your views here.
from django.db.models import Q
from django.shortcuts import render, redirect, resolve_url
from django.http import HttpResponse
from gnews.models import GNews, Video, Advertising, Music
from django.contrib.auth import logout
from index.models import Discount
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage


# Create your views here.

def index(request):
    recommend = GNews.objects.all().order_by('-article_date')[0:6]
    videos = Video.objects.all().order_by('-video_date')[0:6]
    advertising = Advertising.objects.all()
    rec = {'recommend': recommend, 'videos': videos, 'advertising': advertising}
    return render(request, 'index/index.html', rec)


def logout_view(request):
    logout(request)
    return redirect('index')


def music(request):
    music = Music.objects.all()
    return render(request, 'gnews/music.html', {'music': music})


def discount_all(request):
    discount_all = Discount.objects.filter(type='All')
    paginator = Paginator(discount_all, 12, 3)  # 每个页面分12个内容
    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            discount_all = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            discount_all = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            discount_all = paginator.page(paginator.num_pages)
    return render(request, 'index/discount_all.html', {'discount_all': discount_all})


def discount_steam(request):
    discount_all = Discount.objects.filter(type='Steam')
    paginator = Paginator(discount_all, 12, 3)  # 每个页面分12个内容
    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            discount_all = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            discount_all = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            discount_all = paginator.page(paginator.num_pages)
    return render(request, 'index/discount_steam.html', {'discount_all': discount_all})


def discount_switch(request):
    discount_all = Discount.objects.filter(type='Switch')
    paginator = Paginator(discount_all, 12, 3)  # 每个页面分12个内容
    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            discount_all = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            discount_all = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            discount_all = paginator.page(paginator.num_pages)
    return render(request, 'index/discount_switch.html', {'discount_all': discount_all})


def discount_ps(request):
    discount_all = Discount.objects.filter(type='PS4')
    paginator = Paginator(discount_all, 12, 3)  # 每个页面分12个内容
    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            discount_all = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            discount_all = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            discount_all = paginator.page(paginator.num_pages)
    return render(request, 'index/discount_ps.html', {'discount_all': discount_all})


def discount_xbox(request):
    discount_all = Discount.objects.filter(type='Xbox')
    paginator = Paginator(discount_all, 12, 3)  # 每个页面分12个内容
    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            discount_all = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            discount_all = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            discount_all = paginator.page(paginator.num_pages)
    return render(request, 'index/discount_xbox.html', {'discount_all': discount_all})


def search(request):
    if request.POST:
        title = request.POST.get('title')
        if title == '':
            return render(request, 'index/search.html')
        news = GNews.objects.filter(article_title__contains=title)
        videos = Video.objects.filter(video_title__contains=title)
        musics = Music.objects.filter(Q(title__icontains=title) | Q(singer__icontains=title))
        return render(request, 'index/search.html', {'news': news, 'videos': videos, 'musics': musics})
    return render(request, 'index/search.html')
