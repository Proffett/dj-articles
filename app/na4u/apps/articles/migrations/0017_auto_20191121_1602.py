# Generated by Django 2.2.7 on 2019-11-21 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0016_auto_20191120_1914'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='description',
            field=models.CharField(blank=True, max_length=160, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='article',
            name='keywords',
            field=models.CharField(blank=True, max_length=100, verbose_name='keywords'),
        ),
        migrations.AlterField(
            model_name='article',
            name='article_title',
            field=models.CharField(max_length=150, verbose_name='название статьи'),
        ),
    ]
