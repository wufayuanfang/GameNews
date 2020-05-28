from django.forms import ModelForm, forms
from django.contrib.auth.models import User
from captcha.fields import CaptchaField
from .models import UserProfile


class UserModelForm(ModelForm):
    captcha = CaptchaField(required=True, error_messages={'invalid': '验证码错误'})

    class Meta:
        model = User  # 关联的model类
        fields = {'captcha'}  # 或('name','email','user_type')    #验证哪些字段，"__all__"表示所有字段
        exclude = None  # 排除的字段 ("id",)是元组
        labels = None  # 提示信息
        help_texts = None  # 帮助提示信息
        widgets = None  # 自定义插件
        error_messages = None  # 自定义错误信息（整体错误信息from django.core.exceptions import NON_FIELD_ERRORS）
        field_classes = None  # 自定义字段类（也阔以自定义字段）
        localized_fields = ()  # 本地化，根据settings中TIME_ZONE设置的不同时区显示时间


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        # 定义表单包含的字段
        fields = ('phone', 'avatar', 'bio')
