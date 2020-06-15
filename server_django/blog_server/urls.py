"""blog_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from .views import *
from user import urls
from btoken import urls
from topic import urls
from message_self import urls



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^test_api',test_api),
    url(r'v1/users',include('user.urls',namespace='user')),
    #添加btoken模块,url映射,该模块用于登录操作
    url(r'v1/token',include('btoken.urls')),
    url(r'v1/topics',include('topic.urls')),
    url(r'v1/messages',include('message_self.urls'))
]
#添加tu7pian路由映射http://127.0.0.1:8000/media/aaa.jpg
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
