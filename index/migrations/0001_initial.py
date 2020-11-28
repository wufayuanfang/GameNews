# Generated by Django 3.1.2 on 2020-10-26 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imageUrl', models.CharField(max_length=200, verbose_name='封面URL')),
                ('name', models.CharField(max_length=30, verbose_name='游戏名')),
                ('dis', models.CharField(max_length=6, verbose_name='折扣')),
                ('current', models.CharField(max_length=10, verbose_name='现价')),
                ('state', models.CharField(max_length=8, verbose_name='国区')),
                ('original', models.CharField(max_length=10, verbose_name='原价')),
                ('type', models.CharField(choices=[('All', 'All'), ('Steam', 'Steam'), ('Switch', 'Switch'), ('PS4', 'PS4'), ('Xbox', 'Xbox')], default='All', max_length=6)),
            ],
            options={
                'verbose_name': '游戏折扣排行',
                'verbose_name_plural': '游戏折扣排行',
                'db_table': 'discount',
            },
        ),
    ]
