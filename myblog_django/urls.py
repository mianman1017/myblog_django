"""myblog_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myblog_django_app.views import (
    articlelist_get,
    articlelist_tag_get,
    articlelist_search_get,
    article_get,
    messagelist_get,
    message_add,
    postlist_get
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("articlelist/get/", articlelist_get),
    path("articlelist/tag/get/", articlelist_tag_get),
    path("articlelist/search/get/", articlelist_search_get),
    path("article/get/", article_get),
    path("messagelist/get/", messagelist_get),
    path("message/add/", message_add),
    path("postlist/get/", postlist_get)


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
