from django.http import FileResponse, JsonResponse
from myblog_django_app.models import ArticleInfo, UserInfo, MessageInfo, PostInfo, ImgOfPostInfo
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from random import random
import markdown
import re
import smtplib
from email.mime.text import MIMEText

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


# 文章标签查询接口
@csrf_exempt
def articlelist_tag_get(request):
    if request.method == 'POST':
        offset = int(request.POST.get('offset', 0))
        tag = request.POST.get('tag', '')
        if tag:
            articles = ArticleInfo.objects.filter(
                tags__contains=tag).all()[offset:offset+5]

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
        q1.children.append(('title__contains', _input))
        q1.children.append(('tags__contains', _input))
        q1.children.append(('body__contains', _input))

        if _input:
            articles = ArticleInfo.objects.filter(q1).all()[offset:offset+5]

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
            'markdown.extensions.toc',
        ])

        text = article.body

        body = md.convert(text)

        all_latex = re.findall("\$\$(.*?)\$\$", body, re.S)

        for latex in all_latex:
            # print(latex)
            body = body.replace(
                '<p>$${}$$</p>'.format(latex), '<div style="width: 100%;text-align:center"><img src="https://latex.codecogs.com/svg.latex?{}"></div>'.format(latex))

        all_latex = re.findall("\$(.*?)\$", body, re.S)

        for latex in all_latex:
            # print(latex)
            body = body.replace(
                '${}$'.format(latex), '<img style="position:relative;top:5px;" src="https://latex.codecogs.com/svg.latex?{}">'.format(latex))

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
                'createTime': post.createTime,
                'imgs': img_list
            }

            post_list.append(post_dict)

        return JsonResponse({'success': True, 'data': post_list})

    return JsonResponse({'success': False, 'msg': '不是post请求'})
