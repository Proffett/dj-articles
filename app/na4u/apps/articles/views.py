from .models import Article, Comment, Section, Tag, LikeDislike
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.utils import timezone
from django.urls import reverse, reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger #for paginator
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from .forms import LoginForm
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.mixins import LoginRequiredMixin   #login required
from django.contrib.auth.models import User
from django.contrib import auth
from django.views import View
from django.views.generic import View, ListView, CreateView #for post create view
from django.views.generic.detail import DetailView
from .forms import PostForm, CommentForm, TagForm # create post form
import json
from .utils import *
from django.db.models import Q
from django.db.models import Count


#Like/Dislike
class VotesView(View):
    model = None    # Модель данных - Статьи или Комментарии
    vote_type = None # Тип комментария Like/Dislike
 
    def post(self, request, pk):
        obj = self.model.objects.get(pk=pk)
        # GenericForeignKey не поддерживает метод get_or_create
        try:
            likedislike = LikeDislike.objects.get(content_type=ContentType.objects.get_for_model(obj), object_id=obj.id, user=request.user)
            if likedislike.vote is not self.vote_type:
                likedislike.vote = self.vote_type
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except LikeDislike.DoesNotExist:
            obj.votes.create(user=request.user, vote=self.vote_type)
            result = True
 
        return HttpResponse(
            json.dumps({
                "result": result,
                "like_count": obj.votes.likes().count(),
                "dislike_count": obj.votes.dislikes().count(),
                "sum_rating": obj.votes.sum_rating()
            }),
            content_type="application/json"
        )


#article-list view
def index(request):
    
    search_query = request.GET.get('search', '')
    if search_query:
        latest_articles_list = Article.objects.filter(Q(article_title__icontains=search_query) | Q(article_text__icontains=search_query))
    else:
        latest_articles_list = Article.objects.all()

    paginator = Paginator(latest_articles_list, 7)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    form_auth = AuthenticationForm
    return render(request, 'articles/list.html', context={'paginator': page, 'form_auth':form_auth})

# post-article view
# def detail(request, the_slug):
#     try:
#         a = Article.objects.get(slug__iexact=the_slug)
#     except:
#         raise Http404("Страница или статья не найдена")
#     latest_comments_list = a.comment_set.order_by('-id')[:10]
#     form_auth = AuthenticationForm
#     comment_form = CommentForm
#     def get_absolute_url(self):
#         return reverse('detail', kwargs={'the_slug': self.slug})
#     # slug_url_kwarg = 'the_slug'
#     # # Should match the name of the slug field on the model 
#     # slug_field = 'slug' # DetailView's default value: optional
#     return render(request, 'articles/detail.html', context={'article': a, 'latest_comments_list': latest_comments_list, 'form':form_auth, 'comment_form':comment_form})

class PostCreate(LoginRequiredMixin, ObjectCreateMixin, View): # новый
    model_form = PostForm
    template = 'articles/post_create.html'

class PostUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Article # новый
    model_form = PostForm
    template = 'articles/post_update_form.html'
    raise_exception = True
    # def get(self, request):
    #     form = PostForm()
    #     return render(request, 'articles/post_create.html', context={'form':form})

    # def post(self, request):
    #     bound_form = PostForm(request.POST, request.FILES)

    #     if bound_form.is_valid():
    #         new_post = bound_form.save()
    #         return redirect('index')
    #     return render(request, 'articles/post_create.html', context={'form': bound_form})

class PostDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Article # новый
    model_form = PostForm
    template = 'articles/post_delete_form.html'
    raise_exception = True


class PostDetail(ObjectDetailMixin, View, CommentForm):
    model = Article
    template = 'articles/detail.html'
    redirect_url = 'articles:post_detail_url'
    # def get_comment(self, request):
    #     template = 'articles/detail.html'
    #     comment = Article.objects.filter(comment=comment)
    #     return render(request, template, context={'comment': comment})
       
    # def get(self, request, the_slug):
    #     try:
    #         a = Article.objects.get(slug__iexact=the_slug)
    #     except:
    #         raise Http404("Страница или статья не найдена")
    #     latest_comments_list = a.comment_set.order_by('-id')[:10]
    #     form_auth = AuthenticationForm
    #     comment_form = CommentForm
    #     def get_absolute_url(self):
    #         return reverse('detail', kwargs={'the_slug': self.slug})
        # slug_url_kwarg = 'the_slug'
        # # Should match the name of the slug field on the model 
        # slug_field = 'slug' # DetailView's default value: optional
    # return render(request, 'articles/detail.html', context={'article': a, 'latest_comments_list': latest_comments_list, 'form':form_auth, 'comment_form':comment_form})
# class ArticleDetailView(DetailView):

#     model = Article
#     slug_url_kwarg = 'the_slug'
#     # Should match the name of the slug field on the model 
#     slug_field = 'slug' # DetailView's default value: optional
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['now'] = timezone.now()
#         form_auth = AuthenticationForm
#         context['form_auth'] = form_auth
#         return context
 
# request.POST.get("the_slug")
#leave comment view
# def leave_comment(request, the_slug):
#     try:
#         a = Article.objects.get(slug__iexact=the_slug)
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
#     slug_url_kwarg = 'the_slug'
#     # Should match the name of the slug field on the model 
#     slug_field = 'slug' # DetailView's default value: optional
#     # a.comment_set.create(comment_user = comment.comment_user, comment_text = request.POST['text'])
#     return HttpResponseRedirect(reverse('articles:detail', args = (the_slug,)))
# def login(request):
#     if request.method == "POST":
#         form_reg = AuthenticationForm(request.POST)
#         if form_reg.is_valid():
#             user = form_reg.save()
#             return redirect("articles:index")

#     form_auth = AuthenticationForm
#     return render(request, "articles/login.html", context={"form_auth":form_auth})
def user_login(request):
        if request.method == 'POST':        
            form = LoginForm(request.POST)        
            if form.is_valid():            
                cd = form.cleaned_data            
                user = authenticate(request, username=cd['username'], password=cd['password'])        
            if user is not None:            
                if user.is_active:                
                    login(request, user)                
                    return HttpResponse('Authenticated successfully')            
                else:                
                    return HttpResponse('Disabled account')        
            else:            
                return HttpResponse('Invalid login')    
        else:        
            form = LoginForm()    
        return render(request, 'articles/login.html', {'form': form})
        
#registration view
def register(request):
    if request.method == "POST":
        form_reg = UserCreationForm(request.POST)
        if form_reg.is_valid():
            user = form_reg.save()
            username = form_reg.cleaned_data.get('username')
            login(request, user)
            return redirect("articles:index")

        else:
            for msg in form_reg.error_messages:
                print(form_reg.error_messages[msg])

            return render(request, 'articles/register.html', context={"form":form_reg})

    form_reg = UserCreationForm
    form_auth = AuthenticationForm
    return render(request = request,
                  template_name = "articles/register.html",
                  context={"form_reg":form_reg, "form":form_auth})


def tags_list(request):
    tags = Tag.objects.all()
    form_auth = AuthenticationForm

    return render(request, 'articles/tags_list.html', context={'tags': tags, 'form_auth': form_auth})



#не определен для применения, аналог index view 
class HomePageView(ListView):
    model = Article
    template_name = 'articles/list.html'


#create post view
# class CreatePostView(LoginRequiredMixin, CreateView): # новый
#     model = Article
#     form_class = PostForm
#     template_name = 'articles/post.html'
#     success_url = reverse_lazy('index')
class TagDetail(ObjectDetailMixin, View):
    model = Tag
    template = 'articles/tag_detail.html'
    # def get(self, request, the_slug):
    #     tag = get_object_or_404(Tag, slug__iexact=the_slug)
    #     return render(request, 'articles/tag_detail.html', context={'tag': tag})


class TagCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    model_form = TagForm
    template = 'articles/tag_create.html'
    raise_exception = True
    # def get(self, request):
    #     form = TagForm()
    #     return render(request, 'articles/tag_create.html', context={'form':form})

    # def post(self, request):
    #     bound_form = TagForm(request.POST)

    #     if bound_form.is_valid():
    #         new_tag = bound_form.save()
    #         return redirect('/')
    #     return render(request, 'articles/tag_create.html', context={'form': bound_form})


class TagUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Tag
    model_form = TagForm
    template = 'articles/tag_update_form.html'
    raise_exception = True
    # def get(self, request, slug):
    #     tag = Tag.objects.get(slug__iexact=slug)
    #     bound_form = TagForm(instance=tag)
    #     return render(request, 'articles/tag_update_form.html', context={'form': bound_form, 'tag': tag})

    # def post(self, request, slug):
    #     tag = Tag.objects.get(slug__iexact=slug)
    #     bound_form = TagForm(request.POST, instance=tag)

    #     if bound_form.is_valid():
    #         new_tag = bound_form.save()
    #         return redirect('index')
    #     return render(request, 'articles/tag_update_form.html', context={'form': bound_form, 'tag': tag})
class TagDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Tag
    template = 'articles/tag_delete_form.html'
    redirect_url = 'articles:tags_list_url'
    raise_exception = True

    # def get(self, request, slug):
    #     tag = Tag.objects.get(slug__iexact=slug)
    #     return render(request, 'articles/tag_delete_form.html', context={'tag':tag})

    # def post(self, request, slug):
    #     tag = Tag.objects.get(slug__iexact=slug)
    #     tag.delete()
    #     return redirect(reverse('tags_list'))


# class CreateCommentView(LoginRequiredMixin, CreateView): # новый
#     model = Comment
#     form_class = CommentForm
#     template_name = 'articles/commentform.html'
#     success_url = reverse_lazy('articles:detail')
    
# def like(request, pk):
#     obj = Article.objects.get(pk=pk)
#     try:
#         likedislike = LikeDislike.objects.get(content_type=ContentType.objects.get_for_model(obj), object_id=obj.id, user=request.user)
#         if likedislike.vote is not LikeDislike.LIKE:
#             likedislike.vote = LikeDislike.LIKE
#             likedislike.save(update_fields=['vote'])
#             result = True
#         else:
#             likedislike.delete()
#             result = False
#     except LikeDislike.DoesNotExist:
#         obj.votes.create(user=request.user, vote=LikeDislike.LIKE)
#         result = True
    
#     return HttpResponse(
#         json.dumps({
#             "result": result,
#             "like_count": obj.votes.likes().count(),
#             "dislike_count": obj.votes.dislikes().count(),
#             "sum_rating": obj.votes.sum_rating()
#         }),
#         content_type="application/json"
#     )