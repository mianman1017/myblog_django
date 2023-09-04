from django.contrib import admin
from .models import ArticleInfo, MessageInfo, PostInfo, ImgOfPostInfo, FriendsInfo, CommentInfo

# Register your models here.

# 注册ArticlePost到admin中
admin.site.register(ArticleInfo)
admin.site.register(MessageInfo)
admin.site.register(PostInfo)
admin.site.register(ImgOfPostInfo)
admin.site.register(FriendsInfo)
admin.site.register(CommentInfo)
# Register your models here.
