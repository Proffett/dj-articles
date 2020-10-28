"""na4u URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
# from . import views
from .views import redirect_articles
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', redirect_articles),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('articles/', include('articles.urls')),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('grappelli/', include('grappelli.urls')), # grappelli URLS
    path('admin/', admin.site.urls),
    # path('', views.index, name='index'),
    # path('articles/<the_slug>', include('articles.urls'), name='detail'),
    # path('articles/create/', include('articles.urls')),
    # path('articles/<str:slug>/', include('articles.urls')),
    # path('articles/<str:slug>/update/', include('articles.urls')),
    # path('articles/<str:slug>/delete/', include('articles.urls')),
    # path('articles/tags/', include('articles.urls')),
    # path('articles/tag/create/', include('articles.urls')),
    # path('articles/tag/<str:slug>/', include('articles.urls')),
    # path('articles/tag/<str:slug>/update/', include('articles.urls')),
    # path('articles/tag/<str:slug>/delete/', include('articles.urls')),
    # path('articles/tag/<str:the_slug>', views.tag_detail, name='tag_detail_urls'),
    # path('api/v1/', include('likes.api.urls')),
    path('api/', include('articles.urls')),
    path('djrichtextfield/', include('djrichtextfield.urls')),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG: # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 