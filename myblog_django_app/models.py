from django.db import models
from mdeditor.fields import MDTextField
from myblog_django.settings import MEDIA_ADDR
import markdown
import datetime
# Create your models here.


# 文章表
class ArticleInfo(models.Model):
    weight = models.IntegerField(verbose_name='置顶', default=0)
    author = models.CharField(verbose_name='作者', max_length=16)
    title = models.CharField(verbose_name='标题', max_length=100)
    img = models.ImageField(verbose_name='图片', upload_to='ArticlePhotos',
                            default='ArticlePhotos/default.png')
    body = MDTextField(verbose_name='内容')
    summary = models.CharField(verbose_name="摘要", max_length=100)
    tags = models.TextField(
        verbose_name='标签', blank=True, null=True, help_text='用逗号分隔')
    commentCounts = models.IntegerField(verbose_name='评论量', default=0)
    viewCounts = models.IntegerField(verbose_name='浏览量', default=0)
    createDate = models.DateField(
        verbose_name='创建日期', default=datetime.date.today)
    updateDate = models.DateField(
        verbose_name='更新日期', default=datetime.date.today)

    # 按优先置顶、其次创建时间的方式倒序排列
    class Meta:
        ordering = ('-weight', '-createDate',)

    def __str__(self):
        return self.title

    def get_imgUrl(self):
        return MEDIA_ADDR + str(self.img)


# 留言表
class MessageInfo(models.Model):
    top = models.CharField(verbose_name='顶距', max_length=16)
    right = models.CharField(verbose_name='右距', max_length=16, null=True)
    content = models.CharField(verbose_name='内容', max_length=1024)


# 说说表
class PostInfo(models.Model):
    avatar = models.ImageField(verbose_name='头像', upload_to='Avatars',
                               default='Avatars/default.jpg')
    name = models.CharField(verbose_name="昵称", max_length=32)
    content = models.TextField(
        verbose_name='内容', blank=True, null=True)
    createTime = models.DateTimeField(
        verbose_name="时间", default=datetime.datetime.now())

    def get_avatarUrl(self):
        return MEDIA_ADDR + str(self.avatar)

    # 按优先置顶、其次创建时间的方式倒序排列
    class Meta:
        ordering = ('-createTime',)


# 说说图片表
class ImgOfPostInfo(models.Model):
    postid = models.IntegerField(verbose_name='博客ID')
    img = models.ImageField(verbose_name='图片', upload_to='PostPhotos',
                            default='PostPhotos/default.png')

    def get_imgUrl(self):
        return MEDIA_ADDR + str(self.img)


# 友链表
class FriendsInfo(models.Model):
    name = models.CharField(verbose_name="名称", max_length=32, null=True)
    intro = models.CharField(verbose_name="介绍", max_length=128, null=True)
    img = models.ImageField(verbose_name='图片', upload_to='FriendsPhotos',
                            default='FriendsPhotos/default.png')
    link = models.CharField(verbose_name="链接", max_length=256, null=True)

    def get_imgUrl(self):
        return MEDIA_ADDR + str(self.img)


# 评论表
class CommentInfo(models.Model):
    articleid = models.IntegerField(verbose_name='文章id')
    content = models.CharField(verbose_name='内容', max_length=1024)
    createTime = models.DateTimeField(
        verbose_name="时间", default=datetime.datetime.now())

    # 按优先置顶、其次创建时间的方式倒序排列
    class Meta:
        ordering = ('-createTime',)
