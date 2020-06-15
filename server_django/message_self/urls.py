from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'^/(?P<topic_id>[\d]+)$',messages,name='messages'),
]