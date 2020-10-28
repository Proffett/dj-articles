from PIL import Image
from django import forms
from .models import Article, Comment, Tag
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib import auth


class LoginForm(forms.Form):    
    username = forms.CharField()    
    password = forms.CharField(widget=forms.PasswordInput)


class PostForm(forms.ModelForm):
    
    class Meta:
        model = Article
        fields = ['article_title', 'article_text', 'cover', 'tags']

        widgets = {
            'article_title': forms.TextInput(attrs={'class': 'form-control'}),
            # 'article_section': forms.SelectMultiple(attrs={'class': 'form-control'}),
            # 'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'article_text': forms.Textarea(attrs={'class': 'form-control'}),
            'cover': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'})
            }
    
    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()

        if new_slug == ('create' or 'update' or 'delete'):
            raise ValidationError('Slug may not be "create", "update", "delete"')
        return new_slug
        # fields = ['article_title', 'cover', 'article_text', 'article_section', 'article_tags']

        # fields['article_text'].widget.attrs.update({'class':'form-control'})

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']
        widgets = {
            # 'comment_user': forms.Select(attrs={'class': 'form-control'}),
            'comment_text': forms.TextInput(attrs={'class': 'form-control'}),
            }


class TagForm(forms.ModelForm):
    # title = forms.CharField(max_length=50)
    # slug = forms.CharField(max_length=50)
    # title.widget.attrs.update({'class':'form-control'})
    # slug.widget.attrs.update({'class':'form-control'})
    class Meta:
        model = Tag
        fields = ['title', 'slug']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'})
            }

    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()

        if new_slug == ('create' or 'update' or 'delete'):
            raise ValidationError('Slug may not be "create", "update", "delete"')
        if Tag.objects.filter(slug__iexact=new_slug).count():
            raise ValidationError('Slug must be unique. We have "{}" slug already' .format(new_slug))
        return new_slug


# class PostForm(forms.ModelForm):
#     model = Article
#     fileds = ['title', 'slug', 'body', 'tags']

#     widgets = {
#         'title': forms.TextInput(attrs={'class': 'form-control'}),
#         'slug': forms.TextInput(attrs={'class': 'form-control'}),
#         'body': forms.TextInput(attrs={'class': 'form-control'}),
#         'tags': forms.TextInput(attrs={'class': 'form-control'})
#         }
#     def clean_slug(self):
#         new_slug = self.cleaned_data['slug'].lower()

#         if new_slug == 'create':
#             raise ValidationError('Slug may not be "Create"')
#         return new_slug
    # def save(self):
    #     new_tag = Tag.objects.create(title=self.cleaned_data['title'],
    #      slug=self.cleaned_data['slug'])
    #     return new_tag