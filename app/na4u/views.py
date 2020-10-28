from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, reverse


def redirect_articles(request):
    # latest_articles_list = Article.objects.order_by('-pub_date')[:5]
    # return render(request, 'base.html')
    return redirect('articles:index', permanent = True)

def tags_list(request):
    return redirect('/articles/tags/')

def tag_detail(request):
    return redirect('/articles/tag/<str:slug>/')

def tag_create(request):
    return redirect('/articles/tag/create/')

def tag_update(request):
    return redirect('/articles/tag/<str:slug>/update/')

def tag_delete(request):
    return redirect('/articles/tag/<str:slug>/delete/')

def post_detail(request):
    return redirect('/articles/<str:slug>/')

def post_create(request):
    return redirect('/articles/create/')

def post_update(request):
    return redirect('/articles/<str:slug>/update/')

def post_delete(request):
    return redirect('/articles/<str:slug>/delete/')


