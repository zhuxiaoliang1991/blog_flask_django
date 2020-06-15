from django.db import models

# Create your models here.
from topic.models import Topic
from user.models import UserProfile


class Message1(models.Model):
    topic = models.ForeignKey(Topic,related_name='messages',verbose_name='帖子')
    content = models.CharField(max_length=200,verbose_name='内容')
    publisher = models.ForeignKey(UserProfile,related_name='messages',verbose_name='作者')
    created_time = models.DateTimeField(auto_now=True,verbose_name='时间')
    msg_id = models.IntegerField(verbose_name='留言定位',null=True)


    class Meta:
        db_table = 'message1'
        verbose_name = '留言与回复'
        verbose_name_plural = verbose_name

