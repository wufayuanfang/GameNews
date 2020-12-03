import datetime
import threading

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View

from Spider.Cf import spider_cf_begin
from Spider.GCores import spider_gcores_begin
from Spider.GSky import spider_gsky_begin
from Spider.Hpjy import spider_hpjy_begin
from Spider.Lol import spider_lol_begin
from Spider.Youxun import spider_youxun_begin
from gnews.form import GNewsModelForm
from gnews.models import GNews, Video, Poll
from users.seedConfirmCode import make_code, send_code_register, send_change_pass_link
from .form import UserModelForm
from .models import ConfirmString
from utils.permission.auth_superuser import superuser_required


# Create your views here.
def login_view(request):
    if request.POST:
        # 拿到表单提交的信息
        username = request.POST.get('username')
        password = request.POST.get('password')
        # 处理表单信息
        # ID或密码都输入为空时向登录页面反馈
        # 当ID不存在时向登录页面反馈
        user_exists = User.objects.filter(username=username).exists()

        if not user_exists:
            tip = '输入的账号不存在！'
            form = UserModelForm()
            return render(request, 'users/login.html', locals())
        user = authenticate(username=username, password=password)
        # print(user.is_staff)
        user_form = UserModelForm(request.POST)
        if user:
            if user.is_staff is not True:
                tip = '还没有通过邮箱验证!'
                form = UserModelForm()
                return render(request, 'users/login.html', {'tip': tip, 'form': form})
            if user_form.is_valid():
                login(request, user)
                return redirect('setting')
            else:
                tip = '验证码输入错误!'
                form = UserModelForm()
                return render(request, 'users/login.html', {'tip': tip, 'form': form})
        else:
            tip = '密码输入错误!'
            form = UserModelForm()
            return render(request, 'users/login.html', locals())

    form = UserModelForm()

    return render(request, 'users/login.html', {'form': form})


def register(request):
    if request.POST:
        # 拿到注册的数据
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        user_form = UserModelForm(request.POST)
        if not user_form.is_valid():
            tip = '验证码输入错误!'
            form = UserModelForm()
            return render(request, 'users/register.html', {'tip': tip, 'form': form})
            # 添加数据

        user_exists = User.objects.filter(username=username).exists()
        if user_exists:
            tip = '用户已存在！'
            return render(request, 'users/register.html', {'tip': tip})

        email_exists = User.objects.filter(email=email).exists()
        if email_exists:
            User.objects.get(email=email)
            tip = '邮箱已注册！'
            return render(request, 'users/register.html', {'tip': tip})
        else:
            new_user = User.objects.create_user(username=username, password=password, email=email, is_staff=0,
                                                is_active=1)
            new_user.save()
            code = make_code(new_user)  # 创建验证码并拿到验证码
            send_code_register(email, code)  # 把验证码发给注册邮箱

            message = '账号已注册且验证码已发到邮箱，需到邮箱验证后才可登录'
            return render(request, 'users/wating.html', {'message': message, 'title': '注册确认'})
    form = UserModelForm()
    return render(request, 'users/register.html', {'form': form})


# 登录验证拦截
@login_required(login_url='login')
def setting(request):
    today = datetime.datetime.now().strftime('%Y-%m-%d')

    if request.POST:
        user_id = request.POST.get('user_id')
        password_new = request.POST.get('password')
        user = User.objects.get(id=user_id)
        if request.user != user:
            return JsonResponse({'code': 404})
            # 判断Username是否改动而改动
        else:
            request.user.set_password(password_new)
            request.user.save()
            return JsonResponse({'code': 200})

    return render(request, 'users/setting.html', {'today': today})


@superuser_required(to='setting')
def spider(request):
    target = request.GET.get('target')
    spider_date = request.GET.get('spider_date')

    today = datetime.datetime.now().strftime('%Y-%m-%d')
    if spider_date > today:
        messages.warning(request, "输入的日期最大为今天！")
        return redirect('setting')

    if target == 'gcore':
        threading.Thread(target=spider_gcores_begin, args=(spider_date,)).start()
        # spider_gcores_begin(day)
        messages.success(request, "gcores爬虫已经在后台开始!")
        return redirect('setting')
    if target == 'gamesky':
        threading.Thread(target=spider_gsky_begin, args=(spider_date,)).start()
        messages.success(request, "gsky爬虫已经在后台开始!")
        return redirect('setting')
    if target == 'youxun':
        threading.Thread(target=spider_youxun_begin, args=(spider_date,)).start()
        messages.success(request, "youxun已经在后台开始!")
        return redirect('setting')
    if target == 'lol':
        threading.Thread(target=spider_lol_begin, args=(spider_date,)).start()
        messages.success(request, "lol爬虫已经在后台开始!")
        return redirect('setting')
    if target == 'cf':
        threading.Thread(target=spider_cf_begin, args=(spider_date,)).start()
        messages.success(request, "CF爬虫已经在后台开始!")
        return redirect('setting')
    if target == 'hpjy':
        threading.Thread(target=spider_hpjy_begin, args=(spider_date,)).start()
        messages.success(request, "gp爬虫已经在后台开始!")
        return redirect('setting')
    return redirect('setting')


def confirm(request):
    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = ConfirmString.objects.get(code=code)
    except:
        message = '无效的确认请求!'
        return render(request, 'users/wating.html', locals())

    register_time = confirm.register_time
    now = timezone.now()
    if now > register_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = '您的邮件已经过期！请重新注册!'
        return render(request, 'users/wating.html', locals())
    else:
        confirm.user.is_staff = 1
        confirm.user.save()
        confirm.delete()
        message = '感谢确认，请使用账户登录！'
        return render(request, 'users/wating.html', locals())


class ForgotPass(View):
    def get(self, request, *args, **kwargs):
        username = kwargs.get('username')
        code = kwargs.get('code')
        return render(request, 'users/change_password.html', {'username': username, 'code': code})

    def post(self, request, *args, **kwargs):
        password = request.POST.get('password')
        password_again = request.POST.get('password_again')
        username = request.POST.get('username')
        code = request.POST.get('code')

        user = User.objects.filter(username=username).first()

        if not user:
            msg = '此用户不存在'
            return render(request, 'users/wating.html', {'message': msg, 'title': '提示信息'})

        if user.confirmstring.code != code:
            msg = '参数错误，请联系管理员'
            return render(request, 'users/change_password.html', {'message': msg, 'username': username})
        # 判断验证码是否有效
        if password != password_again:
            msg = '两次输入的密码不一致'
            return render(request, 'users/change_password.html', {'username': username, 'code': code, 'message': msg})
        else:
            user.set_password(password)
            # user.password = password
            user.save()  # 保存更改的数据
            user.confirmstring.delete()  # 把验证码删了
            message = '密码修改成功！！！'
            return render(request, 'users/wating.html', {'message': message})


def forgot_password(request):
    if request.POST:
        form = UserModelForm(request.POST)
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if not user:
            tip = '邮箱不存在'
            form = UserModelForm()
            return render(request, 'users/forgotpassword.html', {'tip': tip, 'form': form})

        if form.is_valid():
            msg = '确认码已发送到注册邮箱'
            # form = UserModelForm()
            code = make_code(user)  # 创建验证码并拿到验证码
            # send_code_change_password(email, code)  # 把验证码发给注册邮箱
            send_change_pass_link(email=email, code=code, username=user.username)
            return render(request, 'users/wating.html', {'message': msg, 'title': '提示信息'})
        else:
            tip = '验证码输入错误'
            form = UserModelForm()
            return render(request, 'users/forgotpassword.html', {'tip': tip, 'form': form})

    form = UserModelForm()
    return render(request, 'users/forgotpassword.html', locals())


def editor(request):
    if request.GET:
        editor_type = request.GET.get('type')
        if editor_type == "article":
            form = GNewsModelForm()
            return render(request, 'users/upload_article.html', locals())
        elif editor_type == "":
            pass
        return render(request, 'users/wating.html', {'message': "参数错误", 'title': '注册确认'})


def my_vote(request):
    user_id = request.GET.get('user_id')
    user = User.objects.get(id=user_id)
    polls = Poll.objects.filter(user=user)

    my_article = GNews.objects.filter(article_from=user.username)
    my_video = Video.objects.filter(video_from=user.username)
    return render(request, 'users/vote.html', {'polls': polls, 'my_article': my_article, 'my_video': my_video})
