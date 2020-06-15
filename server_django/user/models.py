from django.db import models


# Create your models here.
class UserProfile(models.Model):
    username = models.CharField(max_length=11,primary_key=True,verbose_name='用户名')
    nickname = models.CharField(max_length=30,verbose_name='昵称')
    email = models.EmailField(max_length=50,verbose_name='邮箱')
    password = models.CharField(max_length=40,verbose_name='密码')
    sign = models.CharField(max_length=50,verbose_name='个人签名')
    info = models.CharField(max_length=150,verbose_name='个人描述')
    avatar = models.ImageField(upload_to='avatar/',verbose_name='头像')

    def __str__(self):
        return self.username


    class Meta:
        db_table = 'user_profile'
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name


