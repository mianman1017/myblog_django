from django.http import FileResponse, JsonResponse
from myblog_django_app.models import ArticleInfo
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import markdown
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
import os
import base64

# Create your views here.


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
        return JsonResponse({'data': article_list, 'success': True})

    return JsonResponse({'success': False, 'msg': 'Invalid request method'})


@csrf_exempt
def article_get(request):
    if request.method == 'POST':
        # 从前端请求中获取偏移值
        id = int(request.POST.get('id', 0))
        print(id)

        # 取出从偏移值开始的博客文章
        print(ArticleInfo.objects.all().first().id)  # 打印出来的结果为1
        article = ArticleInfo.objects.filter(id=id).first()
        print(article.id)

        # 构造 JSON 数据
        tags = article.tags.split(',') if article.tags else []

        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc'
        ])
        body = md.convert(article.body)
        print(body)
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
        return JsonResponse({'data': article_dict, 'success': True})

    return JsonResponse({'success': False, 'msg': 'Invalid request method'})
