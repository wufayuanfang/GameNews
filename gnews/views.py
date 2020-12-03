from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from comments.models import Comment, Comment_vidoe
from gnews.models import GNews, Image_article, News_special, Poll
from gnews.models import Video as Videos
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage


# Create your views here.

class Article(View):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        # 单个文章时
        if pk:
            article = GNews.objects.get(pk=pk)
            # 浏览量 +1
            # update_fields=[]指定了数据库只更新total_views字段，优化执行效率。
            article.total_views += 1
            article.save(update_fields=['total_views'])

            # 获取点赞数
            poll = Poll.objects.filter(article=article)
            vote_num = len(poll)

            try:
                images = Image_article.objects.filter(article_id=article)
                article = {'article': article, 'images': images, 'vote_num': vote_num}
            except:
                article = {'article': article, 'vote_num': vote_num, }

            return render(request, 'gnews/article.html', article)
        else:
            special = News_special.objects.all()[3:6]
            gnews_list = GNews.objects.all().order_by('-article_date')  # 按时间来排序，倒序让时间最早的在前

            article_hot_list = GNews.objects.all().order_by('-total_views')[0:5]
            paginator = Paginator(gnews_list, 12, )

            # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
            page = request.GET.get('page')
            try:
                recommend = paginator.page(page)
            # todo: 注意捕获异常
            except PageNotAnInteger:
                # 如果请求的页数不是整数, 返回第一页。
                recommend = paginator.page(1)
            except EmptyPage:
                # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
                recommend = paginator.page(paginator.num_pages)
            except InvalidPage:
                # 如果请求的页数不存在, 重定向页面
                return HttpResponse('找不到页面的内容')

        return render(request, 'gnews/news.html',
                      {'recommend': recommend, 'special': special, 'article_hot_list': article_hot_list})

    def post(self, request, *args, **kwargs):
        pass


class Video(View):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        # 单查
        if pk:
            video = Videos.objects.get(pk=pk)
            # update_fields=[]指定了数据库只更新total_views字段，优化执行效率。
            video.total_views += 1
            video.save(update_fields=['total_views'])

            comments = Comment_vidoe.objects.filter(video=video)

            # 为评论引入表单
            context = {'video': video, 'comments': comments}

            return render(request, 'gnews/video_click.html', context)
        else:
            video_list = Videos.objects.all().order_by('-video_date')  # 按时间来排序，倒序让时间最早的在前，倒序，最新爬的在前
            paginator = Paginator(video_list, 12)  # 每个页面分12个内容
            # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
            page = request.GET.get('page')
            try:
                videos = paginator.page(page)
            # todo: 注意捕获异常
            except PageNotAnInteger:
                # 如果请求的页数不是整数, 返回第一页。
                videos = paginator.page(1)
            except EmptyPage:
                # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
                videos = paginator.page(paginator.num_pages)
            except InvalidPage:
                # 如果请求的页数不存在, 重定向页面
                return HttpResponse('找不到页面的内容')
        return render(request, 'gnews/video.html', {'videos': videos})


def vote(request):
    user_id = request.GET.get('user_id')
    article_id = request.GET.get('article_id')
    user = User.objects.get(id=user_id)
    article = GNews.objects.get(article_id=article_id)
    if Poll.objects.filter(user=user, article=article).exists():
        messages = '您已点过赞！'
    else:
        poll = Poll(user=user, article=article)
        poll.save()
        messages = '点赞成功！'
    return HttpResponse(messages)
