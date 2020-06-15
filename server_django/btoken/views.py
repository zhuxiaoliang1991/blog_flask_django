import hashlib
import json

import time

import jwt

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from user.models import UserProfile


def btoken(request):

    if request.method == 'POST':
        #创建token
        data_json = request.body
        #如果没有数据
        if not data_json:
            result = {'code':102,'error':'Request is None'}
            return JsonResponse(result)
        else:
            data = json.loads(data_json)
            username = data.get('username')
            password = data.get('password')
            if not username:
                result = {'code':103,'error':'Username not in the request'}
                return JsonResponse(result)
            if not password:
                result = {'code':105,'error':'Password not in the request'}
                return JsonResponse(result)

            users = UserProfile.objects.filter(username=username)
            if not users:
                #用户不存在
                result = {'code':108,'error':'The username is not existed'}
                return JsonResponse(result)
            #hash计算密码值
            h_sha1 = hashlib.sha1()
            h_sha1.update(password.encode())
            password_i = h_sha1.hexdigest()
            if password_i != users[0].password:
                result = {'code':109,'error':'The password is wrong!!!'}
                return JsonResponse(result)
            else:
                token = make_token(username)
                result = {'code':200,'username':username,'data':{'token':token.decode()}}
                return JsonResponse(result)
    else:
        result = {'code':201,'error':'The request method is not POST'}
        return JsonResponse(result)

#生成token
def make_token(username,expire=3600*24):
    key = 'abcdef1234'
    expir = int(time.time()+expire)
    payload = {'username':username,'exp':expir}
    token = jwt.encode(payload,key,algorithm='HS256')
    return token




