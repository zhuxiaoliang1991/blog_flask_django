from django.conf.urls import url
from .views import *

urlpatterns = [
    #/v1/topics/author_id
    url(r'/(?P<author_id>[\w]+)$',topics,name='topics'),
]