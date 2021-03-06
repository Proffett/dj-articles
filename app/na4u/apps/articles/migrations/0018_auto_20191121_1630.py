# Generated by Django 2.2.7 on 2019-11-21 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0017_auto_20191121_1602'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='article_title',
            field=models.CharField(max_length=150, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='article',
            name='cover',
            field=models.ImageField(blank=True, default='images/noimage.png', upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='article',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='public date'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='comment_text',
            field=models.CharField(max_length=200, verbose_name='Comment'),
        ),
    ]
