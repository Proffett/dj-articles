# Generated by Django 2.2.7 on 2019-11-26 18:30

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0019_auto_20191126_1827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='article_text',
            field=ckeditor.fields.RichTextField(verbose_name='post text'),
        ),
    ]