# coding:utf8

from django.db import models

from users.models import UserProfile

# Create your models here.


class Modules(models.Model):
    module_name = models.CharField('板块名称', max_length=10)

    class Meta:
        verbose_name = '板块名称'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.module_name


class Articles(models.Model):
    title = models.CharField('文章名称', max_length=128)
    summary = models.CharField('文章简介', max_length=255)
    favour_count = models.IntegerField('被赞数', default=0)
    comment_count = models.IntegerField('评论数', default=0)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    module = models.ForeignKey(Modules, verbose_name='所属板块')
    user = models.ForeignKey(UserProfile, verbose_name='所属用户', null=True, blank=True)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class ArticleDetail(models.Model):
    article = models.ForeignKey(verbose_name='所属文章', to='Articles')
    content = models.TextField(verbose_name='文章内容')

    class Meta:
        verbose_name = '文章详细'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.article.title


class Comment(models.Model):
    content = models.CharField('评论内容', max_length=255)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    article = models.ForeignKey(verbose_name='评论文章', to='Articles')
    user = models.ForeignKey(UserProfile, verbose_name='评论者')
    reply = models.ForeignKey(verbose_name='回复评论', to='self', related_name='back', null=True, blank=True)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content


class Favour(models.Model):
    article = models.ForeignKey(verbose_name='所赞文章', to='Articles')
    user = models.ForeignKey(UserProfile, verbose_name='赞者')
    favour = models.BooleanField(verbose_name='是否已赞', default=False)

    class Meta:
        verbose_name = '赞'
        verbose_name_plural = verbose_name

