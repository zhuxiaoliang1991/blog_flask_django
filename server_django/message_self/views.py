import json

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from tools.loging_decorator import loging_check

from topic.models import Topic

from message_self.models import Message1


@loging_check('POST')
def messages(request,topic_id):

    if request.method == 'POST':
        #创建 留言/回复
        user = request.user
        json_str = request.body
        if not json_str:
            result = {'code':402,'error':'please give me json str'}
            return JsonResponse(result)
        json_obj = json.loads(json_str)
        #留言内容
        content = json_obj.get('content')
        #父级留言的ID
        msg_id = json_obj.get('parent_id',0)
        if not content:
            result = {'code':403,'error':'please give me content'}
            return JsonResponse(result)
        try:
            topic = Topic.objects.get(id=topic_id)
        except Exception as e:
            result = {'code':404,'error':'This topic is not existed'}
            return JsonResponse(result)
        #判断当前topic limit
        if topic.limit == 'private':
            #如果当前limit是私有的,则必须为博主方可评论
            if user.username == topic.author.username:
                result = {'code':405,'error':'Please go out'}
                return JsonResponse(result)
        Message1.objects.create(topic=topic,content=content,msg_id=msg_id,publisher=user)
        return JsonResponse({'code':200,'data':{}})
