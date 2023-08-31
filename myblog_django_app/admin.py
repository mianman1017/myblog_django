from django.contrib import admin
from .models import ArticleInfo, MessageInfo, PostInfo, ImgOfPostInfo, FriendsInfo

# Register your models here.

# 注册ArticlePost到admin中
admin.site.register(ArticleInfo)
admin.site.register(MessageInfo)
admin.site.register(PostInfo)
admin.site.register(ImgOfPostInfo)
admin.site.register(FriendsInfo)
# Register your models here.
