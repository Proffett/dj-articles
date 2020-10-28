import datetime
from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.db.models import Sum
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.shortcuts import reverse
from time import time
from PIL import Image
from imagekit.models.fields import ImageSpecField
from imagekit.processors import ResizeToFit, Adjust, ResizeToFill
from meta.models import ModelMeta
# from djrichtextfield.models import RichTextField
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField



class Jobseeker(models.Model):
    def get_file_path(self, filename):
        extension = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), extension)
        return os.path.join("images", filename)
        photo = models.ImageField(verbose_name=u'Poster',upload_to=get_file_path,max_length=256, blank=True, null=True)
        photo_small =ImageSpecField([Adjust(contrast=1.2, sharpness=1.1),
            ResizeToFill(50, 50)], image_field='photo',
            format='JPEG', options={'quality': 90})
        photo_medium =ImageSpecField([Adjust(contrast=1.2, sharpness=1.1),
            ResizeToFit(300, 200)], image_field='photo',
            format='JPEG', options={'quality': 90})
        photo_big =ImageSpecField([Adjust(contrast=1.2, sharpness=1.1),
            ResizeToFit(640, 480)], image_field='photo',
            format='JPEG', options={'quality': 90})



class LikeDislikeManager(models.Manager):
    use_for_related_fields = True
 
    def likes(self):
        # Забираем queryset с записями больше 0
        return self.get_queryset().filter(vote__gt=0)
 
    def dislikes(self):
        # Забираем queryset с записями меньше 0
        return self.get_queryset().filter(vote__lt=0)
 
    def sum_rating(self):
        # Забираем суммарный рейтинг
        return self.get_queryset().aggregate(Sum('vote')).get('vote__sum') or 0

    def articles(self):
        return self.get_queryset().filter(content_type__model='article').order_by('-articles__pub_date')
     
    def comments(self):
        return self.get_queryset().filter(content_type__model='comment').order_by('-comments__pub_date')

class LikeDislike(models.Model):
    LIKE = 1
    DISLIKE = -1
 
    VOTES = (
        (DISLIKE, 'Не нравится'),
        (LIKE, 'Нравится')
    )
 
    vote = models.SmallIntegerField(verbose_name="vote", choices=VOTES)
    user = models.ForeignKey(User, verbose_name="user", on_delete = models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete = models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    objects = LikeDislikeManager()


def gen_slug(self):
    new_slug = slugify(self, allow_unicode=True)
    return new_slug + '-' + str(int(time()))


class Section(models.Model):
        class Meta:
            db_table = "section"
     
        section_title = models.CharField(max_length=200)
        section_url = models.CharField(max_length=50)
        section_description = models.TextField('текст раздела')
        slug = models.SlugField(max_length=200, blank=True, unique=True)
        
        def __str__(self):
            return self.section_title


class Article(ModelMeta, models.Model):
    article_title = models.CharField('title', max_length = 150)
    description = models.CharField('description', blank=True, max_length = 160)
    keywords = models.CharField('keywords', blank=True, max_length = 100)
    article_text = RichTextUploadingField('post text')
    author = models.ForeignKey(User, verbose_name="author", default = 1, on_delete = models.CASCADE)
    article_section = models.ForeignKey(Section, on_delete = models.CASCADE, blank=True, default=1)
    slug = models.SlugField(max_length=200, blank=True, unique=True)
    pub_date = models.DateTimeField('public date', auto_now_add=True)
    cover = models.ImageField(upload_to='images/', blank=True, default='images/noimage.png')
    tags = models.ManyToManyField('Tag', blank=True, related_name='articles')
    comments = models.ManyToManyField('Comment', blank=True, related_name='comment_article')
    # context_object_name = 'articles'
    votes = GenericRelation(LikeDislike, related_query_name='articles')
    thumbnail = ImageSpecField(source='cover',
                                      processors=[ResizeToFill(270, 180)],
                                      format='JPEG',
                                      options={'quality': 60})
    class Media:
        js = [
            '/static/ckeditor/ckeditor-init.js',
        ]
    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ['-pub_date']

    _metadata = {
        'title': 'article_title',
        'description': 'description',
        'keywords': 'keywords',
        'cover': 'get_meta_image'
    }
    def get_meta_image(self):
        if self.cover:
            return self.cover.url


    def get_absolute_url(self):
        return reverse('articles:post_detail_url', kwargs = {'slug' : self.slug})

    def get_update_url(self):
        return reverse('articles:post_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('articles:post_delete_url', kwargs={'slug': self.slug})

    def post_delete_url(self):
        return reverse('articles:post_delete_url', kwargs={'slug': self.slug})

    def was_published_recently(self):
        return self.pub_date >= (timezone.now() - datetime.timedelta(days = 7))

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.article_title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.article_title


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete = models.CASCADE, default=None)
    comment_user = models.ForeignKey(User, on_delete = models.CASCADE, default=None)
    comment_text = models.CharField('Comment', max_length = 200)
    pub_date = models.DateTimeField('comment date', auto_now_add=True)
    votes = GenericRelation(LikeDislike, related_query_name='comments')

    def __str__(self):
        return self.comment_text


    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ['-pub_date']



class Tag(models.Model):
    title = models.CharField(max_length = 50)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ['title']
        
    def get_absolute_url(self):
        return reverse('articles:tag_detail_url', kwargs = {'slug' : self.slug})
    
    def get_update_url(self):
        return reverse('articles:tag_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('articles:tag_delete_url', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title
