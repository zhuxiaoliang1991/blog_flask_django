import jwt
#*methods - 可接受任意参数
#**kwargs - 可接受多个key=value形式的参数
from django.http import JsonResponse

from user.models import UserProfile

KEY = "abcdef1234"

def loging_check(*methods):
    def _loging_check(func):
        def wrapper(request,*args,**kwargs):
            #token 放在 request header -> authorization
            #request.META.get('HTTP_AUTHORIZATION')
            token = request.META.get('HTTP_AUTHORIZATION')
            if not methods:
                #如果没有传methods参数,则直接返回视图
                return func(request,*args,**kwargs)
            else:
                #methods 有值
                if not request.method in methods:
                    #如果请求的方法不在methods内,则直接返回视图
                    return func(request,*args,**kwargs)
                    #严格判断参数大小写,统一大写
                    #严格检查methods里面的参数是POST,GET,PUT,DELETE
                else:
                     # 判断当前的method是否在*methods中,则进行token校验
                    if not token or token == 'null':
                        result = {'code':'107','error':'Please give me token'}
                        return JsonResponse(result)
                    else:
                        # 校验token,pyjwt注意 异常检测
                        try:
                            res = jwt.decode(token,KEY,algorithms='HS256')
                        except Exception as e:
                            print('----token error is %s-----'%e)
                            result = {'code':'108','error':'Please login'}
                            return JsonResponse(result)
                        # token校验成功,,根据用户名取出用户
                        username = res['username']
                        user = UserProfile.objects.get(username=username)
                        # request.user = user
                        request.user = user
            return func(request,*args,**kwargs)
        return wrapper
    return _loging_check


def get_user_by_request(request):
    #通过request获取用户,要么返回user对象,要么返回None
    token = request.META.get('HTTP_AUTHORIZATION')
    #检查token
    if not token or token == 'null':
        return None
    try:
        res = jwt.decode(token,KEY,algorithms='HS256')
    except Exception as e:
        print('-----get_user_by_request -jwt decode error is %s'%e)
        return None
    # 获取token中的用户名
    username = res['username']
    user = UserProfile.objects.get(username=username)
    return user

