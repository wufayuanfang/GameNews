from django.db import models
from ckeditor.fields import RichTextField  # 富文本编辑器
from django.contrib.auth.models import User


# Create your models here.

class GNews(models.Model):
    article_id = models.AutoField(primary_key=True, verbose_name='文章ID')
    article_title = models.CharField(max_length=50, verbose_name='文章标题', unique=True)
    article_date = models.DateField(verbose_name='文章时间')
    article_cover = models.CharField(max_length=200, verbose_name='文章封面')
    article_contents = RichTextField(verbose_name='文字内容')
    # article_contents = models.CharField(max_length=10000, verbose_name='文字内容')
    article_from = models.CharField(max_length=50, verbose_name='文章来源')
    article_video = models.CharField(max_length=300, verbose_name='文章视频', null=True)

    # 文章除了文本以外应该有图片等信息，因为不同文章的图片数量是不一致的，所以用一对多映射来关联文章的图片

    # 点击量
    total_views = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'gnews'  # 修改了表名
        verbose_name = '文章'
        verbose_name_plural = verbose_name  # 指定模型的复数形式是什么,如果不指定Django会自动在模型名称后加一个’s’

    def __str__(self):
        return self.article_title


class Image_article(models.Model):
    gnews = models.ForeignKey(GNews, verbose_name='来源文章', on_delete=models.CASCADE)
    image_title = models.CharField(max_length=50, verbose_name='图片标题', null=True)
    image_links = models.CharField(max_length=200, verbose_name='图片链接')

    class Meta:
        db_table = 'news_image'  # 修改了表名
        verbose_name = '文章图片'
        verbose_name_plural = verbose_name  # 指定模型的复数形式是什么,如果不指定Django会自动在模型名称后加一个’s’

    def __str__(self):
        return self.image_title


class Video(models.Model):
    video_title = models.CharField(max_length=50, verbose_name='视频标题', unique=True)
    video_date = models.DateField(verbose_name='视频时间')
    video_from = models.CharField(max_length=10, verbose_name='视频类型', default='other')
    video_link = models.CharField(max_length=400, verbose_name='视频链接')

    # 点击量
    total_views = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'video'  # 修改了表名
        verbose_name = '视频'
        verbose_name_plural = verbose_name  # 指定模型的复数形式是什么,如果不指定Django会自动在模型名称后加一个’s’

    def __str__(self):
        return self.video_title


class News_special(models.Model):
    article = models.ForeignKey(GNews, verbose_name='专题文章', on_delete=models.CASCADE)

    # video = models.ForeignKey(Video, verbose_name='')

    class Meta:
        db_table = 'news_special'  # 修改了表名
        verbose_name = '专题文章'
        verbose_name_plural = verbose_name  # 指定模型的复数形式是什么,如果不指定Django会自动在模型名称后加一个’s’


class Advertising(models.Model):
    ad_title = models.CharField(max_length=50, verbose_name='广告标题')
    ad_cover = models.CharField(max_length=200, verbose_name='广告封面')
    ad_link = models.CharField(max_length=200, verbose_name='广告链接')

    class Meta:
        db_table = 'advertising'  # 修改了表名
        verbose_name = '广告'
        verbose_name_plural = verbose_name  # 指定模型的复数形式是什么,如果不指定Django会自动在模型名称后加一个’s’


class Music(models.Model):
    title = models.CharField(max_length=50, verbose_name='歌名')
    singer = models.CharField(max_length=50, verbose_name='歌手', default='未知歌手')
    songUrl = models.CharField(max_length=200, verbose_name='歌曲链接')
    imageUrl = models.CharField(max_length=200, verbose_name='歌曲图片链接', null=True,
                                default='http://127.0.0.1:8000/media/img/demo.jpg')

    class Meta:
        db_table = 'music'  # 修改了表名
        verbose_name = '专题音乐'
        verbose_name_plural = verbose_name  # 指定模型的复数形式是什么,如果不指定Django会自动在模型名称后加一个’s’


class Poll(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='点赞的用户')
    article = models.ForeignKey(GNews, on_delete=models.CASCADE, verbose_name='点赞的文章')

    class Meta:
        db_table = 'poll'  # 修改了表名
        verbose_name = '点赞表'
        verbose_name_plural = verbose_name  # 指定模型的复数形式是什么,如果不指定Django会自动在模型名称后加一个’s’
