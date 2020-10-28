from . import views
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from .models import Article, Comment, LikeDislike, Tag
from .views import * # new


app_name = 'articles'

urlpatterns = [
    path('', index, name = 'index'),
    path('create/', PostCreate.as_view(), name = 'post_create_url'),
    path('articles/<str:slug>/', PostDetail.as_view(), name = 'post_detail_url'),
    path('articles/<str:slug>/update/', PostUpdate.as_view(), name = 'post_update_url'),
    path('articles/<str:slug>/delete/', PostDelete.as_view(), name = 'post_delete_url'),
    path('<str:slug>/leave_comment', PostDetail.as_view(), name = 'leave_comment'),
    path('register/', register, name='register'),
    path('login/', views.user_login, name='login'),
    path('api/v1/', include('likes.api.urls')),
    path('tags/', tags_list, name='tags_list_url'),
    path('tag/create/', TagCreate.as_view(), name='tag_create_url'),
    path('tag/<str:slug>/', TagDetail.as_view(), name='tag_detail_url'),
    path('tag/<str:slug>/update/', TagUpdate.as_view(), name='tag_update_url'),
    path('tag/<str:slug>/delete/', TagDelete.as_view(), name='tag_delete_url'),
    path('<str:slug>/article/like/',
        login_required(views.VotesView.as_view(model=Article, vote_type=LikeDislike.LIKE)),
        name='article_like'),
    re_path(r'^article/(?P<pk>\d+)/dislike/$',
        login_required(views.VotesView.as_view(model=Article, vote_type=LikeDislike.DISLIKE)),
        name='article_dislike'),
    re_path(r'^comment/(?P<pk>\d+)/like/$',
        login_required(views.VotesView.as_view(model=Comment, vote_type=LikeDislike.LIKE)),
        name='comment_like'),
    re_path(r'^comment/(?P<pk>\d+)/dislike/$',
        login_required(views.VotesView.as_view(model=Comment, vote_type=LikeDislike.DISLIKE)),
        name='comment_dislike'),
    # path('api/', views.VotesView.as_view(), name='api'),
]

if settings.DEBUG: # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
