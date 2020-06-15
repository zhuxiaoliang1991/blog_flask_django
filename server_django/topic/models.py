from datetime import time
from django.db import models
from user.models import UserProfile

# Create your models here.
class Topic(models.Model):
    title = models.CharField(max_length=50,verbose_name='文章标题')
    author = models.ForeignKey(UserProfile,related_name='topics',verbose_name='作者')
    category = models.CharField(max_length=20,choices=(('no-tec','非技术'),('tec','技术')),default='tec',verbose_name='分类')
    limit = models.CharField(max_length=10,choices=(('public','公开'),('private','私密')),default='public',verbose_name='是否发布')
    created_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    modified_time = models.DateTimeField(auto_now=True,verbose_name='更改时间')
    content = models.TextField(verbose_name='内容')
    introduce = models.CharField(max_length=90,verbose_name='内容简介')


    def __str__(self):
        return self.title

    class Meta:
        db_table = 'topic'
        verbose_name = '帖子'
        verbose_name_plural = verbose_name

