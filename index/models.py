from django.db import models


# Create your models here.


class Game(models.Model):
    title = models.CharField(max_length=50, verbose_name='游戏名')
    description = models.CharField(max_length=400, verbose_name="描述")
    cover = models.CharField(max_length=200, verbose_name="封面")
    released_at = models.CharField(max_length=20, verbose_name="发售时间")

    class Meta:
        db_table = 'game'  # 修改了表名
        verbose_name = '游戏'
        verbose_name_plural = verbose_name  # 指定模型的复数形式是什么,如果不指定Django会自动在模型名称后加一个’s’


class GamePrice(models.Model):
    area_name = models.CharField(max_length=20, verbose_name='地区')
    source_currency = models.CharField(max_length=5, verbose_name="货币单位")
    source_amount = models.CharField(max_length=10, verbose_name="原价")
    amount = models.CharField(max_length=10, verbose_name="现价")

    class Meta:
        db_table = 'game_price'  # 修改了表名
        verbose_name = '游戏价格'
        verbose_name_plural = verbose_name  # 指定模型的复数形式是什么,如果不指定Django会自动在模型名称后加一个’s’
