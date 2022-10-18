# Generated by Django 4.1.1 on 2022-10-05 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_blogcategory_blogpage_categories'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpage',
            name='webranking',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='blogpage',
            name='weburl',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]
