# Generated by Django 2.2.4 on 2019-11-18 18:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0014_auto_20191118_1803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='article_section',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='articles.Section'),
        ),
    ]
