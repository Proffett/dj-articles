from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from .forms import CommentForm
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm


class ObjectDetailMixin:
        model = None
        template = None
        form_auth = AuthenticationForm

        def get(self, request, slug, **kwargs):
            # comments = self.model.comment_articles.all()
            obj = get_object_or_404(self.model, slug__iexact=slug)
            if self.model == Article:
                meta = obj.as_meta(self.request)
                form = CommentForm()
                comments = Comment.objects.filter(article_id=obj)
                return render(request, self.template, context={self.model.__name__.lower(): obj,
                'admin_object': obj, 'detail': True, 'form': form, 'comments':comments, 'form_auth':self.form_auth, 'meta': meta})
            return render(request, self.template, context={self.model.__name__.lower(): obj,
            'admin_object': obj, 'detail': True, 'form_auth':self.form_auth })
        # def get_context_data(self, **kwargs):
        #     context = super(ObjectDetailMixin, self).get_context_data(self, **kwargs)
        #     context['meta'] = self.get_object().as_meta(self.request)
        #     return context
        
        def post(self, request, slug):
            post = get_object_or_404(self.model, slug__iexact=slug)
            # comment_user = request.user
            # article_id = pk
            # data = {'article': pk, 'comment_user': comment_user}
            bound_form = CommentForm(request.POST)
            # bound_form.has_changed()
            if bound_form.is_valid():
                new_obj = bound_form.save(commit=False)
                new_obj.comment_user = request.user
                new_obj.article = post
                new_obj.save()
                return redirect(post)
            return render(request, self.template, context={'form': bound_form}) 
        # def leave_comment(self, request, slug):
        #     try:
        #         a = self.model.objects.get(slug__iexact=slug)
        #     except:
        #         raise Http404("Страница или статья не найдена")
        #     # comment = Comment()
        #     username = request.user.username
        #     user = User.objects.get(username)
        #     a.comment_set.create(comment_user = user, comment_text = request.POST['text'])
        #     # form = CommentForm(request.POST)
        #     # comment.comment_text = request.POST['text']
        #     # comment.comment_user = auth.get_user(request)
        #     # comment.article_id = article_id
        #     # a.comment_set.create(comment_user = comment.comment_user, comment_text = request.POST['text'])
        #     return HttpResponseRedirect(reverse('articles:detail', args = (slug,)))
 

class ObjectCreateMixin:
    model_form = None
    template = None

    def get(self, request):
        form = self.model_form()
        return render(request, self.template, context={'form':form})

    def post(self, request):
        bound_form = self.model_form(request.POST, request.FILES)

        if bound_form.is_valid():
            new_obj = bound_form.save(commit=False)
            new_obj.author = request.user
            new_obj.save()
            return redirect(new_obj)
        return render(request, self.template, context={'form': bound_form})


class ObjectUpdateMixin:
    model = None
    model_form = None
    template = None

    def get(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        bound_form = self.model_form(instance=obj)
        return render(request, self.template, context={'form': bound_form, self.model.__name__.lower(): obj})
        
    def post(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        bound_form = self.model_form(request.POST, instance=obj)
        if bound_form.is_valid():
            new_obj = bound_form.save()
            return redirect(new_obj)
        return render(request, self.template, context={'form': bound_form, self.model.__name__.lower(): obj})

class ObjectDeleteMixin:
    model = None
    template = None
    redirect_url = None

    def get(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        return render(request, self.template, context={self.model.__name__.lower(): obj})
        
    def post(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        obj.delete()
        return redirect(reverse(self.redirect_url))