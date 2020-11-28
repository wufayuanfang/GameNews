import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GameNews.settings")
django.setup()
import random
import time
from users.models import ConfirmString
from django.core.mail import send_mail


def make_code(user):  # 生成随机字符串
    data = "1234567890zxcvbnmlkjhgfdsaqwertyuiop"
    # 用时间来做随机播种
    random.seed(time.time())
    # 随机选取数据
    sa = []
    for i in range(20):
        sa.append(random.choice(data))
    salt = ''.join(sa)
    try:
        ConfirmString.objects.create(code=salt, user=user)
    except:
        con = ConfirmString.objects.get(user=user)
        con.code = salt
        con.save()
    return salt


def send_code_register(email, code):
    subject = '来自xx游戏资讯的注册确认邮件'
    message = '验证信息请不要告诉他人！'
    from_email = 'xx游戏资讯<dfd888@qq.com>'
    recipient_list = [email, ]
    html_message = '''
                    <p>感谢注册<a href="http://{}/users/confirm/?code={}" target=blank>xxx资讯网站</a>，\
                    这里是xx资讯网站！</p>
                    <p>请点击站点链接完成注册确认！</p>
                    <p>此链接有效期为7天！</p>'''.format('127.0.0.1:8000', code)

    send_mail(subject, message, from_email, recipient_list, fail_silently=False, html_message=html_message)


def send_code_change_password(email, code):
    subject = '来自xx游戏资讯的修改密码邮件'
    message = '验证码请不要告诉他人！验证码：' + code
    from_email = 'xx游戏资讯<dfd888@qq.com>'
    recipient_list = [email, ]

    send_mail(subject, message, from_email, recipient_list, fail_silently=False, )


def send_change_pass_link(email, code, username):
    subject = '来自xx游戏资讯 账户密码重置'
    message = '验证信息请不要告诉他人，如果不是您操作请无视该邮件！'
    from_email = 'noreply<dfd888@qq.com>'
    recipient_list = [email, ]
    html_message = '''
    <p>我们收到了您的重置密码请求，请确认重置，选择新的密码。如不进行重置，请忽略此邮件</p>
    <a href="http://{}/users/change_pass/{}/{}" target=blank>重置密码</a>
    <p>请点击站点链接修改密码！</p>'''.format('127.0.0.1:8000', username, code)

    send_mail(subject, message, from_email, recipient_list, fail_silently=False, html_message=html_message)


if __name__ == '__main__':
    make_code()
