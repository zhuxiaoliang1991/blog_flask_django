from django.core.serializers import serialize
from django.http import JsonResponse
from django.shortcuts import render
from user.models import *
from tools.loging_decorator import loging_check

from user.models import UserProfile

from tools.loging_decorator import get_user_by_request

from message_self.models import Message1
from .models import *
import json
# Create your views here.


@loging_check('POST','DELETE')
def topics(request,author_id=None):
    #发博客
    if request.method == "POST":
        #发表博客必须为登录状态
        #当前token中认证通过的用户即为作者
        username = request.user.username
        data = json.loads(request.body)
        if not data:
            result = {'code':302,'error':'Please give me json'}
            return JsonResponse(result)
        title = data['title']
        category = data['category']
        limit = data['limit']
        content = data['content']
        content_text = data['content_text']
        introduce = content_text[:90]
        try:
            topic = Topic.objects.create(title=title,category=category,limit=limit,content=content,introduce=introduce,author=request.user)
        except Exception:
            result = {'code':403,'error':'inserted data into mysql is wrong'}
            return JsonResponse(result)
        topic.save()
        result = {'code':200,'username':username}
        return JsonResponse(result)

    #查看博客
    elif request.method == 'GET':
        #获取用户博客列表或者具体博客内容[带>t_id=xx]
        #1.访问当前博客的 访问者 -visitor
        #2.当前博客的博主 -author

        #博客列表
        authors = UserProfile.objects.filter(username=author_id)
        if not authors:
            result = {'code':305,'error':'The current author is not existed'}
            return JsonResponse(result)
        # 当前访问的博客的博主
        author = authors[0]
        visiter = get_user_by_request(request)
        visiter_username = None
        if visiter:
            visiter_username = visiter.username
        category = request.GET.get('category')
        t_id = request.GET.get('t_id')

        #对比两者的username是否一致,从而判断当前是否要取private的博客
        if visiter_username == author_id:
            if t_id:
                try:
                    author_topic = Topic.objects.get(id=t_id)
                except Exception as e:
                    result = {'code':309,'error':'not topic'}
                    return JsonResponse(result)
                res = make_topic_res(author,author_topic)
                return JsonResponse(res)
            # 博主在访问自己的博客,此时获取用户全部权限的博客
            if category:
                #如果/v1/topics/zhuxiaolian?category=tex|no-tec
                author_topics = Topic.objects.filter(author=author,category=category)
            else:
                #如果/v1/topics/zhuxiaolian
                author_topics = Topic.objects.filter(author=author)
        else:
            if t_id:
                try:
                    author_topic = Topic.objects.get(id=t_id,limit='public')
                except Exception as e:
                    result = {'code': 309, 'error': 'not topic'}
                    return JsonResponse(result)
                #生成具体返回
                res = make_topic_res(author, author_topic,limit='public')
                return JsonResponse(res)
            # 其他访问者在访问当前博客
            if category:
                # 如果/v1/topics/zhuxiaolian?category=tex|no-tec
                author_topics = Topic.objects.filter(author=author,limit='public',category=category)

            else:
                # 如果/v1/topics/zhuxiaolian
                author_topics = Topic.objects.filter(author=author,limit='public')
        res = make_topics_res(author,author_topics)
        return JsonResponse(res)

    #删除博客
    elif request.method == 'DELETE':
        #删除博主的文章
        user = request.user
        if user.username != author_id:
            result = {'code':306,'error':'You can not do it '}
            return JsonResponse(result)
        #当token中的用户名和url中的author_id严格一致:方可删除
        topic_id = request.GET.get('topic_id')
        if not topic_id:
            result = {'code':307,'errot':'You can not do it'}
            return JsonResponse(result)
        try:
            topic = Topic.objects.filter(id=topic_id)[0]
        except Exception as e:
            result = {'code':405,'error':'The topic is not existed'}
            return JsonResponse(result)
        topic.delete()

        result = {'code':200}
        return JsonResponse(result)




def make_topics_res(author,author_topics):
    res = {'code':200,'data':{}}
    topics_res = []
    for topic in author_topics:
        d = {}
        d['id'] = topic.id
        d['title'] = topic.title
        d['category'] = topic.category
        d['created_time'] = topic.created_time.strftime('%Y-%m-%d %H:%M:%S')
        d['introduce'] = topic.introduce
        d['author'] = author.nickname
        topics_res.append(d)
    res['data']['topics'] = topics_res
    res['data']['nickname'] = author.nickname
    return res


def make_topic_res(author,author_topic,limit=None):
    '''
    生成具体的博客内容的返回值
    :param author:
    :param author_topic:
    :return:
    '''
    #next 当前博客的下一个
    if not limit:
        #博主只访问自己
        next_topic = Topic.objects.filter(id__gt=author_topic.id,author=author).first()
        #取出ID小于当前博客ID的数据的最后一个
        last_topic = Topic.objects.filter(id__lt=author_topic.id,author=author).last()
    else:
        #游客访问
        next_topic = Topic.objects.filter(id__gt=author_topic.id,limit=limit,author=author).first()
        last_topic = Topic.objects.filter(id__lt=author_topic.id, limit=limit, author=author).last()
    # 判断下一个是否存在
    if next_topic:
        # 下一个博客内容的id
        next_id = next_topic.id
        # 下一个博客内容的title
        next_title = next_topic.title
    else:
        next_id = None
        next_title = None
    # 判断上一个是否存在
    if last_topic:
        # 上一个博客内容的id
        last_id = last_topic.id
        # 上一个博客内容的title
        last_title = last_topic.title
    else:
        last_id = None
        last_title = None

    messages = Message1.objects.filter(topic=author_topic,msg_id=0).order_by('-created_time')
    messages_list = []
    i = 0
    for message in messages:
        # 每一条留言都封装成一个字典
        message_dict = {}
        message_dict['id'] = message.id
        message_dict['content'] = message.content
        message_dict['publisher'] = message.publisher.nickname
        message_dict['publisher_avatar'] = str(message.publisher.avatar)
        message_dict['created_time'] = message.created_time.strftime('%Y-%m-%d %H:%M:%S')
        replys = Message1.objects.filter(msg_id=message.id)
        # 多条回复放在列表
        reply_list = []
        for reply in replys:
            reply_dict = {}
            reply_dict['publisher'] = reply.publisher.nickname
            reply_dict['publisher_avatar'] = str(reply.publisher.avatar)
            reply_dict['created_time'] = reply.created_time.strftime('%Y-%m-%d %H:%M:%S')
            reply_dict['content'] = reply.content
            reply_dict['msg_id'] = reply.msg_id
            reply_list.append(reply_dict)
        message_dict['reply'] =reply_list
        messages_list.append(message_dict)
        i += 1
    result = {'code':200,'data':{'nickname':author.nickname,'title':author_topic.title,'category':author_topic.category,
                                 'created_time':author_topic.created_time.strftime('%H-%m-%d'),
                                 'content':author_topic.content,'introduce':author_topic.introduce,'author':author.nickname,
                                 'next_id':next_id,'next_title':next_title,'last_id':last_id,'last_title':last_title,
                                 'messages':messages_list,'messages_count':i}}
    return result