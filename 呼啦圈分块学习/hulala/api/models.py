from django.db import models


# Create your models here.


class Category(models.Model):
    '''
    类别
    '''
    name = models.CharField(verbose_name='类别', max_length=32)


class Article(models.Model):
    '''
    文章
    '''
    name = models.CharField(verbose_name='标题', max_length=32)
    content = models.TextField(verbose_name='内容')
    category = models.ForeignKey(to='Category', on_delete=models.CASCADE)
    tag = models.ManyToManyField(to='Tag', verbose_name='标签', blank=True, null=True, default=None)


class Tag(models.Model):
    label = models.CharField(verbose_name='标签', max_length=32)
