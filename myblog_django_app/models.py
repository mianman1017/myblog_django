from django.db import models
from mdeditor.fields import MDTextField
import markdown
import datetime
# Create your models here.


# 文章表
class ArticleInfo(models.Model):

    weight = models.IntegerField(verbose_name='置顶', default=0)
    author = models.CharField(verbose_name='作者', max_length=16)
    title = models.CharField(verbose_name='标题', max_length=100)
    img = models.ImageField(verbose_name='图像', upload_to='ArticlePhotos',
                            default='myblog_django/media/ArticlePhotos/default.png')
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
        MEDIA_ADDR = 'http://localhost:8000/media/'
        return MEDIA_ADDR + str(self.img)


# 用户表
class UserInfo(models.Model):
    email = models.CharField(verbose_name='邮箱', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=32)
    avatar = models.ImageField(verbose_name='头像', upload_to='PersonalPhotos',
                               default='myblog_django/media/PersonalPhotos/avatar.jpg')
    name = models.CharField(verbose_name='昵称', max_length=32)
    website = models.CharField(verbose_name='个人网址', max_length=128)
    motto = models.CharField(verbose_name='个性签名', max_length=128)


# 留言表
class MessageInfo(models.Model):
    top = models.CharField(verbose_name='顶距', max_length=16)
    right = models.CharField(verbose_name='右距', max_length=16, null=True)
    content = models.CharField(verbose_name='内容', max_length=1024)
