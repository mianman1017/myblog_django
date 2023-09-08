from django.http import FileResponse, JsonResponse
from myblog_django_app.models import (
    ArticleInfo,
    UserInfo,
    MessageInfo,
    PostInfo,
    ImgOfPostInfo,
    FriendsInfo,
    CommentInfo
)
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from random import random
import markdown
import re
import smtplib
import datetime
from email.mime.text import MIMEText
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension

# Create your views here.


# 文章列表获取接口
@csrf_exempt
def articlelist_get(request):
    if request.method == 'POST':
        # 从前端请求中获取偏移值
        offset = int(request.POST.get('offset', 0))

        # 取出从偏移值开始的博客文章
        articles = ArticleInfo.objects.all()[offset:offset+5]

        # 构造 JSON 数据
        article_list = []
        for article in articles:
            # print(article)
            tags = article.tags.split(',') if article.tags else []

            article_dict = {
                'id': article.id,
                'weight': article.weight,
                'author': article.author,
                'title': article.title,
                'img': article.get_imgUrl(),
                'body': article.body,
                'summary': article.summary,
                'tags': tags,
                'commentCounts': article.commentCounts,
                'viewCounts': article.viewCounts,
                'createDate': article.createDate.strftime('%Y-%m-%d'),
                'updateDate': article.updateDate.strftime('%Y-%m-%d'),
            }
            article_list.append(article_dict)

        # 返回 JSON 数据
        return JsonResponse({'success': True, 'data': article_list})

    return JsonResponse({'success': False, 'msg': '不是POST请求'})


@csrf_exempt
def article_view_add(request):
    if request.method == 'POST':
        id = int(request.POST.get('id', 0))
        print(id)

        viewCounts = ArticleInfo.objects.filter(id=id).first().viewCounts

        ArticleInfo.objects.filter(id=id).update(viewCounts=viewCounts+1)

        # 返回 JSON 数据
        return JsonResponse({'success': True, 'msg': '浏览量增加成功'})

    return JsonResponse({'success': False, 'msg': '不是POST请求'})


# 文章标签查询接口
@csrf_exempt
def articlelist_tag_get(request):
    if request.method == 'POST':
        offset = int(request.POST.get('offset', 0))
        tag = request.POST.get('tag', '')
        if tag:
            articles = ArticleInfo.objects.filter(
                tags__contains=tag).all()

            # 构造 JSON 数据
            article_list = []
            for article in articles:
                tags = article.tags.split(',') if article.tags else []

                article_dict = {
                    'id': article.id,
                    'weight': article.weight,
                    'author': article.author,
                    'title': article.title,
                    'img': article.get_imgUrl(),
                    'body': article.body,
                    'summary': article.summary,
                    'tags': tags,
                    'commentCounts': article.commentCounts,
                    'viewCounts': article.viewCounts,
                    'createDate': article.createDate.strftime('%Y-%m-%d'),
                    'updateDate': article.updateDate.strftime('%Y-%m-%d'),
                }
                article_list.append(article_dict)

            # 返回 JSON 数据
            return JsonResponse({'success': True, 'data': article_list})
        else:
            return JsonResponse({'success': False, 'msg': '结果为空'})

    return JsonResponse({'success': False, 'msg': '不是POST请求'})


# 文章搜索接口
@csrf_exempt
def articlelist_search_get(request):
    if request.method == 'POST':
        offset = int(request.POST.get('offset', 0))
        _input = request.POST.get('input', '')

        q1 = Q()
        q1.connector = 'OR'
        q1.children.append(('title__icontains', _input))
        q1.children.append(('tags__icontains', _input))
        q1.children.append(('body__icontains', _input))

        if _input:
            articles = ArticleInfo.objects.filter(q1).all()

            # 构造 JSON 数据
            article_list = []
            for article in articles:
                tags = article.tags.split(',') if article.tags else []

                article_dict = {
                    'id': article.id,
                    'weight': article.weight,
                    'author': article.author,
                    'title': article.title,
                    'img': article.get_imgUrl(),
                    'body': article.body,
                    'summary': article.summary,
                    'tags': tags,
                    'commentCounts': article.commentCounts,
                    'viewCounts': article.viewCounts,
                    'createDate': article.createDate.strftime('%Y-%m-%d'),
                    'updateDate': article.updateDate.strftime('%Y-%m-%d'),
                }
                article_list.append(article_dict)

            # 返回 JSON 数据
            return JsonResponse({'success': True, 'data': article_list})
        else:
            return JsonResponse({'success': False, 'msg': '结果为空'})

    return JsonResponse({'success': False, 'msg': '不是POST请求'})


# 文章获取接口
@csrf_exempt
def article_get(request):
    if request.method == 'POST':
        # 从前端请求中获取偏移值
        title = request.POST.get('title', 0)
        # print(id)

        # 取出从偏移值开始的博客文章
        # print(ArticleInfo.objects.all().first().id)  # 打印出来的结果为1
        article = ArticleInfo.objects.filter(title=title).first()
        # print(article.id)

        # 构造 JSON 数据
        tags = article.tags.split(',') if article.tags else []

        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify),
        ])

        text = article.body

        body = md.convert(text)

        all_latex = re.findall("\$\$(.*?)\$\$", body, re.S)

        for latex in all_latex:
            # print(latex)
            body = body.replace(
                '<p>$${}$$</p>'.format(latex), '<div style="width: 100%;text-align:center"><img id="latex" src="https://www.zhihu.com/equation?tex={}"></div>'.format(latex))

        all_latex = re.findall("\$(.*?)\$", body, re.S)

        for latex in all_latex:
            # print(latex)
            body = body.replace(
                '${}$'.format(latex), '<img id="latex" style="vertical-align:middle" src="https://www.zhihu.com/equation?tex={}">'.format(latex))

        # print(body)

        # print(body)
        article_dict = {
            'id': article.id,
            'weight': article.weight,
            'author': article.author,
            'title': article.title,
            'img': article.get_imgUrl(),
            'body': body,
            'toc': md.toc,
            'summary': article.summary,
            'tags': tags,
            'commentCounts': article.commentCounts,
            'viewCounts': article.viewCounts,
            'createDate': article.createDate.strftime('%Y-%m-%d'),
            'updateDate': article.updateDate.strftime('%Y-%m-%d'),
        }

        # 返回 JSON 数据
        return JsonResponse({'success': True, 'data': article_dict})

    return JsonResponse({'success': False, 'msg': '不是POST请求'})


# 留言列表获取接口
@csrf_exempt
def messagelist_get(request):
    if request.method == 'POST':

        # 取出从偏移值开始的博客文章
        messages = MessageInfo.objects.all()

        # 构造 JSON 数据
        message_list = []
        for message in messages:
            message_dict = {
                'id': message.id,
                'top': message.top,
                'content': message.content
            }
            message_list.append(message_dict)

        # 返回 JSON 数据
        return JsonResponse({'success': True, 'data': message_list})

    return JsonResponse({'success': False, 'msg': '不是POST请求'})


# 留言添加接口
@csrf_exempt
def message_add(request):
    if request.method == 'POST':

        message = request.POST.get('message')
        top = request.POST.get('top')
        right = request.POST.get('right')

        if message:
            MessageInfo.objects.create(
                top=top,
                right=right,
                content=message
            )
            return JsonResponse({'success': True, 'msg': '添加成功'})
        else:
            return JsonResponse({'success': False, 'msg': '检测到信息为空'})

    return JsonResponse({'success': False, 'msg': '不是POST请求'})


# 博客列表获取接口
@csrf_exempt
def postlist_get(request):
    if request.method == 'POST':

        offset = int(request.POST.get('offset', 0))
        posts = PostInfo.objects.all()[offset:offset+7]

        post_list = []
        for post in posts:

            imgs = ImgOfPostInfo.objects.filter(postid=post.id).all()
            img_list = []
            for img in imgs:
                img_list.append(img.get_imgUrl())

            post_dict = {
                'avatar': post.get_avatarUrl(),
                'name': post.name,
                'content': post.content,
                'createTime': post.createTime.strftime("%Y-%m-%d %H:%M"),
                'imgs': img_list
            }
            post_list.append(post_dict)

        return JsonResponse({'success': True, 'data': post_list})

    return JsonResponse({'success': False, 'msg': '不是post请求'})


# 友链列表获取接口
@csrf_exempt
def friendlist_get(request):
    if request.method == 'POST':

        # offset = int(request.POST.get('offset', 0))
        friends = FriendsInfo.objects.all()

        friend_list = []
        for friend in friends:
            # print(friend.get_img_data())
            friend_list.append({
                'link': friend.link,
                'img': friend.get_imgUrl(),
                'intro': friend.intro,
                'name': friend.name
            })

        return JsonResponse({'success': True, 'data': friend_list})

    return JsonResponse({'success': False, 'msg': '不是post请求'})


# 评论列表获取接口
@csrf_exempt
def commentlist_get(request):
    if request.method == 'POST':

        id = int(request.POST.get('id', 0))
        comments = CommentInfo.objects.filter(articleid=id).all()

        comment_list = []
        for comment in comments:
            comment_list.append({
                'createTime': comment.createTime.strftime("%Y-%m-%d %H:%M"),
                'content': comment.content,
            })

        return JsonResponse({'success': True, 'data': comment_list})

    return JsonResponse({'success': False, 'msg': '不是post请求'})


# 评论添加接口
@csrf_exempt
def comment_add(request):
    if request.method == 'POST':

        id = int(request.POST.get('id', 0))
        content = request.POST.get('content')
        coummentCounts = ArticleInfo.objects.filter(
            id=id).first().commentCounts
        ArticleInfo.objects.filter(id=id).update(
            commentCounts=coummentCounts+1)
        CommentInfo.objects.create(
            articleid=id, content=content)

        return JsonResponse({'success': True, 'msg': '添加成功'})

    return JsonResponse({'success': False, 'msg': '不是post请求'})
