from django.db import models


# Create your models here.

class Discount(models.Model):
    GAME_DISCOUNT_TYPE_CHOICES = (
        ('All', 'All'),
        ('Steam', 'Steam'),
        ('Switch', 'Switch'),
        ('PS4', 'PS4'),
        ('Xbox', 'Xbox'),
    )
    imageUrl = models.CharField(max_length=200, verbose_name='封面URL')  # 封面
    name = models.CharField(max_length=30, verbose_name='游戏名')  # 游戏名
    dis = models.CharField(max_length=6, verbose_name='折扣')  # 折扣
    current = models.CharField(max_length=10, verbose_name='现价')  # 现价
    state = models.CharField(max_length=8, verbose_name='国区')  # 国区
    original = models.CharField(max_length=10, verbose_name='原价')  # 原价
    type = models.CharField(max_length=6, choices=GAME_DISCOUNT_TYPE_CHOICES, default='All')

    class Meta:
        db_table = 'discount'  # 修改了表名
        verbose_name = '游戏折扣排行'
        verbose_name_plural = verbose_name  # 指定模型的复数形式是什么,如果不指定Django会自动在模型名称后加一个’s’
