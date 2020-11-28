# Create your views here.
from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage, EmptyPage
from django.views import View
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, JsonResponse
from gnews.models import GNews, Video
from comments.models import Comment, Comment_vidoe
from django.contrib.auth.models import User
from comments.forms import Comment_vidoeForm
import json


class Discuss(View):
    def get(self, request, *args, **kwargs):
        pk = request.GET.get('article_id')
        article = GNews.objects.get(pk=pk)
        page = request.GET.get('page')
        comments = Comment.objects.filter(article=article).order_by('created_time').reverse()
        paginator = Paginator(comments, 7, 3)
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1

        try:
            comments = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            comments = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return JsonResponse({'data': None})
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            comments = paginator.page(paginator.num_pages)
        content = [{'user': tmp.user.username, 'created_time': tmp.created_time, 'text': tmp.text, 'comment_id': tmp.id}
                   for tmp in
                   comments.object_list]
        return JsonResponse({'data': content, 'num_pages': paginator.num_pages})

    def delete(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))
        comment_id = data.get('comment_id')
        if comment_id:
            comment_obj = Comment.objects.get(id=comment_id)
            # 删除前先做权限认证，判断删除的评论是否为真实的用户
            comment_obj.delete()
            return JsonResponse({'code': 200, 'meg': '删除成功'})
        else:
            return JsonResponse({'code': 400, 'meg': '删除失败'})

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))
        comment_text = data.get('comment')  # 评论内容
        article_id = data.get('article_id')  # 文章ID，
        user_id = data.get('user_id')  # 评论用户id

        article = GNews.objects.get(article_id=article_id)
        user = User.objects.get(id=user_id)

        if not article_id or not user or not comment_text:
            return JsonResponse({'code': 400, 'msg': '参数错误'})
        comment_obj = Comment(user=user, text=comment_text, article=article)
        comment_obj.save()
        content = {'user': comment_obj.user.username, 'created_time': comment_obj.created_time,
                   'text': comment_obj.text, 'comment_id': comment_obj.id}
        return JsonResponse({'code': 200, 'data': content, 'msg': '评论成功！'})


def comment_video_del(request):
    if request.GET:
        comment_id = request.GET.get('comment_id')
        comment = Comment_vidoe.objects.get(id=comment_id)

        # 删除前先做权限认证，判断删除的评论是否为真实的用户
        comment.delete()
    return HttpResponse()


def post_comment(request):
    # article = get_object_or_404(ArticlePost, id=article_id)
    # 处理 POST 请求
    if request.method == 'POST':
        parent_comment_id = request.POST.get('comment_id')
        video_id = request.POST.get('video_id')
        comment = request.POST.get('comment')
        user_id = request.POST.get('user_id')

        # video_id = int(video_id)
        print(video_id)
        video = Video.objects.get(id=video_id)
        user = User.objects.get(id=user_id)

        # 二级回复
        if parent_comment_id is not None:
            parent_comment = Comment_vidoe.objects.get(id=parent_comment_id)
            # 若回复层级超过二级，则转换为二级
            new_comment_parent_id = parent_comment.get_root().id
            # 被回复人
            new_comment_reply_to = parent_comment.user

            Comment_vidoe.objects.create(video=video, user=user, text=comment,
                                         parent_id=new_comment_parent_id,
                                         reply_to=new_comment_reply_to)
            return JsonResponse({"code": "200 OK", "new_comment_id": video.id})

        Comment_vidoe.objects.create(video=video, user=user, text=comment)
        url = reverse('getvideo') + "?video_id=" + video_id
        return redirect(url)
    # 处理 GET 请求
    elif request.method == 'GET':
        comment_form = Comment_vidoeForm()
        video_id = request.GET.get('video_id')
        parent_comment_id = request.GET.get('comment_id')

        context = {
            'comment_form': comment_form,
            'video_id': video_id,
            'parent_comment_id': parent_comment_id
        }
        return render(request, 'comments/reply.html', context)
    # 处理其他请求
    else:
        return HttpResponse("仅接受GET/POST请求。")
