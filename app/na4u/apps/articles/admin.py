from django.contrib import admin

from .models import Article, Section, Comment, LikeDislike, LikeDislikeManager, Tag


from django.db import models
from ckeditor.fields import RichTextField



@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    article_text = RichTextField()
    # class Media:
    # js = [
    #     '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
    #     '/static/path/to/your/tinymce_setup.js',
    # ]


# admin.site.register(Article)
admin.site.register(Section)
admin.site.register(Comment)
admin.site.register(LikeDislike)
admin.site.register(Tag)