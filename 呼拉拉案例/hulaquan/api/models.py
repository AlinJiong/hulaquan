from django.db import models

# Create your models here.

'''呼啦圈表设计
表：
用户：用户名、密码
评论: 时间、父评论（自关联）、归属文章：评论 1：n、评论者（用户）：评论 1：n
文章: 作者（用户)：文章 1：n 、时间、分类、标题、内容、简介、评论数、浏览数
'''


class UserInfo(models.Model):
    '''用户表'''
    username = models.CharField(verbose_name='用户名', max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)

    def is_authenticated(self):
        pass


class Article(models.Model):
    '文章表'
    category_choices = (
        (1, '咨询'),
        (2, '公司动态'),
        (3, '分享'),
        (4, '答疑'),
        (5, '其他'),
    )
    category = models.IntegerField(verbose_name='分类', choices=category_choices)
    title = models.CharField(verbose_name='标题', max_length=255)
    image = models.CharField(verbose_name='图片路径', max_length=128)
    summary = models.CharField(verbose_name='简介', max_length=255)

    comment_count = models.IntegerField(verbose_name='评论数', default=0)
    read_count = models.IntegerField(verbose_name='阅读数', default=0)

    date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    author = models.ForeignKey(
        to='UserInfo', verbose_name='作者', on_delete=models.CASCADE)


class ArticleDetail(models.Model):
    article = models.OneToOneField(
        verbose_name='文章', to='Article', on_delete=models.CASCADE)
    content = models.TextField(verbose_name='内容')


class Comment(models.Model):
    '评论表'
    content = models.TextField(verbose_name='评论')

    article = models.ForeignKey(
        verbose_name='文章', to='Article', on_delete=models.CASCADE)
    user = models.ForeignKey(
        verbose_name='评论者', to='UserInfo', on_delete=models.CASCADE)
