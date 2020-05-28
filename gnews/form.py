from django.forms import ModelForm
from .models import GNews


class GNewsModelForm(ModelForm):
    class Meta:
        model = GNews  # 关联的model类
        fields = {'article_title', 'article_contents'}  # 或('name','email','user_type')    #验证哪些字段，"__all__"表示所有字段
        exclude = None  # 排除的字段 ("id",)是元组
        labels = None  # 提示信息
        help_texts = None  # 帮助提示信息
        widgets = None  # 自定义插件
        error_messages = None  # 自定义错误信息（整体错误信息from django.core.exceptions import NON_FIELD_ERRORS）
        field_classes = None  # 自定义字段类（也阔以自定义字段）
        localized_fields = ()  # 本地化，根据settings中TIME_ZONE设置的不同时区显示时间
