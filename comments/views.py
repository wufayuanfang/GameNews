from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, JsonResponse

# Create your views here.
from gnews.models import GNews, Video
from comments.models import Comment, Comment_vidoe
from django.contrib.auth.models import User
from comments.forms import Comment_vidoeForm
from gnews.views import getvideo


def comment(request):
    if request.POST:
        comment_text = request.POST.get('comment')  # 评论内容
        article_id = request.POST.get('article_id')  # 文章ID，
        usern_id = request.POST.get('user_id')  # 评论用户名

        article = GNews.objects.get(article_id=article_id)
        user = User.objects.get(id=usern_id)
        comment = Comment(user=user, text=comment_text, article=article)
        comment.save()
        # print(usern_id, article_id, comment_text)
    return redirect('/gnews/getnews/?article_id={}'.format(article_id))


def comment_del(request):
    if request.GET:
        comment_id = request.GET.get('comment_id')
        comment = Comment.objects.get(id=comment_id)

        # 删除前先做权限认证，判断删除的评论是否为真实的用户
        comment.delete()
    return HttpResponse()


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
