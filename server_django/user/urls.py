from django.conf.urls import url
from .views import *


app_name = 'user'
urlpatterns = [
    url(r'^$',users,name='users'),
    #/v1/user/zhuxiaolian
    url(r'/(?P<username>[\w]{1,11})/avatar$',user_avatar, name='avatar'),
    url(r'/(?P<username>[\w]{1,11})$',users,name='user'),

 ]
