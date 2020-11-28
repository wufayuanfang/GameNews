import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 数据库
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'djangonews',  # 数据库名
        'USER': 'root',  # 这里写用户名
        'PASSWORD': 'abc123',  # 密码
        'HOST': '120.24.7.237',  # 数据库所在主机的ip，如果是本机就写localhost
        'PORT': '3307',  # 端口号，默认3306,
    }
}

# 邮箱
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_SSL = True
EMAIL_HOST = 'smtp.qq.com'  # 如果是 163 改成 smtp.163.com
EMAIL_PORT = 465
EMAIL_HOST_USER = 'dfd888@qq.com'  # 帐号
EMAIL_HOST_PASSWORD = 'sgvtllrvdnglbfij'  # 密码
# 收件人看到的发件人
EMAIL_FROM = 'xx游戏资讯<dfd888@qq.com>'

CONFIRM_DAYS = 7

# 腾讯云储存
# 设置用户属性, 包括secret_id, secret_key, region
# appid已在配置中移除,请在参数Bucket中带上appid。Bucket由bucketname-appid组成
COS_SECRETID = 'AKIDykGWXOSnJp78sqCSRBwHSXNJ0SeIdWlF'  # 替换为用户的secret_id
COS_SECRETKEY = 'av0qopdDWR8ZN8fx0NiussnUgcjnebO8'  # 替换为用户的secret_key
COS_REGION = 'ap-guangzhou'  # 替换为用户的region
COS_BUCKET = 'game-news-1302382572'
