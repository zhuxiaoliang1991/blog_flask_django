import jwt
import time
from django.http import JsonResponse
from django.shortcuts import render
import json,hashlib

from btoken.views import make_token

from tools.loging_decorator import loging_check
from .models import *


# Create your views here.
@loging_check('PUT','DELETE')
def users(request,username=None):
    if request.method == 'GET':
        #取数据
        if username:
            #具体用户查询
            #/v1/users/zhuxiaolian?info=1
            #获取全部参数
            try:
                user = UserProfile.objects.filter(username=username)[0]
            except Exception:
                result = {'code':208,'error':'The username is not existed'}
                return JsonResponse(result)
            nickname = user.nickname
            sign = user.sign
            avatar = user.avatar
            info = user.info
            params = request.GET.keys()
            if params:
                data = {}
                for param in params:
                    #数据库中最好是有飞控默认值
                    if hasattr(user,param):
                        data[param] = param
                    result = {'code':200,'username':username,'data':data}
                    return JsonResponse(result)
            else:
                result = {'code':200,'username':username,'data':{'nickname':nickname,'sign':sign,'avatar':str(avatar),'info':info}}
                return JsonResponse(result)

        else:
            #全体用户数据
            users = UserProfile.objects.all()
            res = []
            for user in users:
                username = user.username
                nickname = user.nickname
                sign = user.sign
                avatar = user.avatar
                info = user.info
                resu = {'username':username,'nickname': nickname, 'sign': sign, 'avatar': str(avatar), 'info': info}
                res.append(resu)
            result = {'code':200,'data':res}
            return JsonResponse(result)

    elif request.method == 'POST':
        #注册用户
        #密码需要用SHA-1 hashlib.sha1() -> update ->hexdigest()
        json_str = request.body
        if not json_str:
            #前段异常提交,空数据
            result = {'code':'202','error':'Please POST data'}
            return JsonResponse(result)
        #反序列化json 转为python字符串
        data = json.loads(json_str)
        username = data.get('username')
        if not username:
            #用户不存在
            result = {'code':'203','error':'Please give me username'}
            return JsonResponse(result)
        email = data.get('email')
        if not email:
            #email不存在
            result = {'code':'203','error':'Please give me email'}
            return JsonResponse(result)
        # 检查用户是否存在
        old_user = UserProfile.objects.filter(username=username)
        if old_user:
            # 该用户已经注册
            result = {'code': '207', 'error': 'The username is existed!!'}
        password1 = data.get('password_1')
        password2 = data.get('password_2')
        if not password1 or not password2:
            #密码1和密码2不存在
            result = {'code':'203','error':'Please give me password'}
            return JsonResponse(result)
        if password1 == password2:
            sha = hashlib.sha1()
            sha.update(password1.encode())
            password = sha.hexdigest()
            try:
                UserProfile.objects.create(username=username,nickname=username,email=email,password=password)
            except Exception as e:
                print('UserProfile create error is %s'%(e))
                result = {'code': '207', 'error': 'The username is existed!!'}
                return JsonResponse(result)
            # make_token,根据用户名,生成token
            token = make_token(username)
            result = {'code': '200', 'username': username, 'data': {'token': token.decode()}}
            return JsonResponse(result)
        else:
            result = {'code':'206','error':'The password is wrong!'}
            return JsonResponse(result)

    elif request.method == 'PUT':
        #修改用户数据
        data_json = request.body
        if not data_json:
            result = {'code':202,'error':'The requested data is none'}
            return JsonResponse(result)
        else:
            data = json.loads(data_json)
            nickname = data.get('nickname','')
            sign = data.get('sign','')
            info = data.get('info','')
            user = request.user
            user.nickname = nickname
            user.sign = sign
            user.info = info
            user.save()
            result = {'code':200,'username':username}
            return JsonResponse(result)

    elif request.method == 'DELETE':
        user = request.user
        user.delete()
        result = {'code':200}
        return JsonResponse(result)


@loging_check('POST')
def user_avatar(request,username):
    #上传图片思路
    '''
    1.前端 ->
    :param request:
    :return:
    '''
    # if not request.method == 'POST':
    #     result = {'code':210,'error':'Please use POST'}
    #     return JsonResponse(result)
    # else:
    #     users = UserProfile.objects.filter(username=username)
    # if not users:
    #     result = {'code':208,'error':'The user is not existed'}
    #     return JsonResponse(result)
    user = request.user
    if request.FILES.get('avatar'):
        user.avatar = request.FILES.get('avatar')
        user.save()
        result = {'code':200,'username':username}
        return JsonResponse(result)
    else:
        result = {'code':211,'error':'Please give me avatar'}
        return JsonResponse(result)

