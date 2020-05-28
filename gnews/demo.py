from django.core.mail import send_mail
import DjangoNews.settings

subject = '验证码'
message = '文字内容'
from_email = 'xx游戏资讯<dfd888@qq.com>'
recipient_list = ['dfd888@qq.com', ]
html_message = '带有H5标签的消息内容'

send_mail(subject, message, from_email, recipient_list, fail_silently=False, )
from django.core.mail import send_mail

# send_mail(
#     'Subject here',
#     'Here is the message.',
#     'from@example.com',
#     ['to@example.com'],
#     fail_silently=False,
# )
