# Generated by Django 4.1.1 on 2022-10-11 05:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0016_webpage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='webpage',
            name='categories',
        ),
        migrations.RemoveField(
            model_name='webpage',
            name='tags',
        ),
    ]
