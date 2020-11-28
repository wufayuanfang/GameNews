# Generated by Django 3.1.2 on 2020-10-26 08:22

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Advertising',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ad_title', models.CharField(max_length=50, verbose_name='广告标题')),
                ('ad_cover', models.CharField(max_length=200, verbose_name='广告封面')),
                ('ad_link', models.CharField(max_length=200, verbose_name='广告链接')),
            ],
            options={
                'verbose_name': '广告',
                'verbose_name_plural': '广告',
                'db_table': 'advertising',
            },
        ),
        migrations.CreateModel(
            name='GNews',
            fields=[
                ('article_id', models.AutoField(primary_key=True, serialize=False, verbose_name='文章ID')),
                ('article_title', models.CharField(max_length=50, unique=True, verbose_name='文章标题')),
                ('article_date', models.DateField(verbose_name='文章时间')),
                ('article_cover', models.CharField(max_length=200, verbose_name='文章封面')),
                ('article_contents', ckeditor.fields.RichTextField(verbose_name='文字内容')),
                ('article_from', models.CharField(max_length=50, verbose_name='文章来源')),
                ('article_video', models.CharField(max_length=300, null=True, verbose_name='文章视频')),
                ('total_views', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name': '文章',
                'verbose_name_plural': '文章',
                'db_table': 'gnews',
            },
        ),
        migrations.CreateModel(
            name='Music',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='歌名')),
                ('singer', models.CharField(default='未知歌手', max_length=50, verbose_name='歌手')),
                ('songUrl', models.CharField(max_length=200, verbose_name='歌曲链接')),
                ('imageUrl', models.CharField(default='http://127.0.0.1:8000/media/img/demo.jpg', max_length=200, null=True, verbose_name='歌曲图片链接')),
            ],
            options={
                'verbose_name': '专题音乐',
                'verbose_name_plural': '专题音乐',
                'db_table': 'music',
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_title', models.CharField(max_length=50, unique=True, verbose_name='视频标题')),
                ('video_date', models.DateField(verbose_name='视频时间')),
                ('video_from', models.CharField(default='other', max_length=10, verbose_name='视频类型')),
                ('video_link', models.CharField(max_length=400, verbose_name='视频链接')),
                ('total_views', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name': '视频',
                'verbose_name_plural': '视频',
                'db_table': 'video',
            },
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gnews.gnews', verbose_name='点赞的文章')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='点赞的用户')),
            ],
            options={
                'verbose_name': '点赞表',
                'verbose_name_plural': '点赞表',
                'db_table': 'poll',
            },
        ),
        migrations.CreateModel(
            name='News_special',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gnews.gnews', verbose_name='专题文章')),
            ],
            options={
                'verbose_name': '专题文章',
                'verbose_name_plural': '专题文章',
                'db_table': 'news_special',
            },
        ),
        migrations.CreateModel(
            name='Image_article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_title', models.CharField(max_length=50, null=True, verbose_name='图片标题')),
                ('image_links', models.CharField(max_length=200, verbose_name='图片链接')),
                ('gnews', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gnews.gnews', verbose_name='来源文章')),
            ],
            options={
                'verbose_name': '文章图片',
                'verbose_name_plural': '文章图片',
                'db_table': 'news_image',
            },
        ),
    ]
