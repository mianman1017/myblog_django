# Generated by Django 4.1 on 2023-08-03 07:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("myblog_django_app", "0003_remove_articleinfo_tag"),
    ]

    operations = [
        migrations.AddField(
            model_name="articleinfo",
            name="img",
            field=models.ImageField(
                default="../default.png", upload_to="ArticlePhotos", verbose_name="图像"
            ),
        ),
    ]