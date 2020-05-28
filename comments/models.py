from django.db import models
from django.utils import timezone
from gnews.models import GNews, Video
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey


# Create your models here.
class Comment(models.Model):
    user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE)
    text = models.TextField(verbose_name='内容')
    created_time = models.DateTimeField('创建时间', default=timezone.now)

    article = models.ForeignKey(GNews, verbose_name='关联文章', on_delete=models.CASCADE)

    class Meta:
        db_table = 'comment'  # 修改了表名
        verbose_name = '文章评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{}: {}'.format(self.user.username, self.text[:20])


class Comment_vidoe(MPTTModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(verbose_name='内容')
    created_time = models.DateTimeField('创建时间', default=timezone.now)

    video = models.ForeignKey(Video, verbose_name='关联视频', on_delete=models.CASCADE)

    # 新增，mptt树形结构
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    # 新增，记录二级评论回复给谁, str
    reply_to = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replyers'
    )

    # 替换 Meta 为 MPTTMeta
    # class Meta:
    #     ordering = ('created',)
    class MPTTMeta:
        order_insertion_by = ['created_time']

