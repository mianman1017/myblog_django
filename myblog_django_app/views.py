from django.http import FileResponse, JsonResponse
from myblog_django_app.models import ArticleInfo, UserInfo, MessageInfo
from django.views.decorators.csrf import csrf_exempt
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


# 文章获取接口
@csrf_exempt
def article_get(request):
    if request.method == 'POST':
        # 从前端请求中获取偏移值
        id = int(request.POST.get('id', 0))
        # print(id)

        # 取出从偏移值开始的博客文章
        # print(ArticleInfo.objects.all().first().id)  # 打印出来的结果为1
        article = ArticleInfo.objects.filter(id=id).first()
        # print(article.id)

        # 构造 JSON 数据
        tags = article.tags.split(',') if article.tags else []

        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc'
        ])
        body = md.convert(article.body)
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


# 邮箱格式验证的正则表达式
EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$'


@csrf_exempt
def user_add(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # 检查邮箱格式是否有效
        if not re.match(EMAIL_REGEX, email):
            return JsonResponse({'success': False, 'message': '邮箱格式错误'})

        # 使用SMTP验证检查邮箱是否真实存在
        if not is_valid_email(email):
            return JsonResponse({'success': False, 'message': '邮箱不存在'})

        UserInfo.objects.create(email=email, password=password)

        return JsonResponse({'success': True, 'message': '成功创建用户'})

    return JsonResponse({'success': False, 'message': '不是POST请求'})


def is_valid_email(email):
    try:
        server = smtplib.SMTP('smtp.aliyun.com')  # 替换为你的SMTP服务器
        server.verify(email)
        server.quit()
        return True
    except smtplib.SMTPRecipientsRefused:
        return False
