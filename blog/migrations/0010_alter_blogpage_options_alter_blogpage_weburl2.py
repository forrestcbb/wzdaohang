# Generated by Django 4.1.1 on 2022-10-05 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_blogpage_weburl2'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogpage',
            options={'ordering': ['-webranking']},
        ),
        migrations.AlterField(
            model_name='blogpage',
            name='weburl2',
            field=models.URLField(blank=True, verbose_name='网址：'),
        ),
    ]
