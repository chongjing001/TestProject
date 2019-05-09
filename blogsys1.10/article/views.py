from django.core.paginator import Paginator
from django.shortcuts import render

from django.http import HttpResponseRedirect, JsonResponse

# Create your views here.
from django.urls import reverse

from article.forms import ArticleForm
from article.models import Article, Part
from utils.functions import is_login


# @is_login
def index(request):
    if request.method == 'GET':
        page = int(request.GET.get('page', 1))
        articles = Article.objects.all()
        count = len(articles)
        pg = Paginator(articles, 5)
        articles = pg.page(page)
        flag = 'article'
        return render(request, 'article.html', {'articles': articles,'count':count,'flag':flag})


def add_article(request):
    if request.method == 'GET':
        parts = Part.objects.all()
        return render(request, 'add_article.html', {'parts': parts})
    if request.method == 'POST':
        # 获取内容
        title = request.POST.get('title')
        part = request.POST.get('part')
        tags = request.POST.get('tags')
        content = request.POST.get('content')
        icon = request.FILES.get('icon')
        if not all([title, content]):
            msg = '标题、栏目和内容必填'
            return render(request, 'add_article.html', {'msg': msg})
        # 创建文章
        Article.objects.create(a_title=title,
                               a_part=part,
                               a_tag=tags,
                               content=content,
                               icon=icon)
        return HttpResponseRedirect(reverse('article:index'))


# form表单

# def add_article(request):
#     if request.method == 'GET':
#         return render(request, 'add_article.html')
#     if request.method == 'POST':
#         form = ArticleForm(request.POST, request.FILES)
#         if form.is_valid():
#             title = form.cleaned_data['title']
#             part = form.cleaned_data['part']
#             tags = form.cleaned_data['tags']
#             content = form.cleaned_data['content']
#             icon = form.cleaned_data['icon']
#             Article.objects.create(a_title=title,
#                                    a_part=part,
#                                    a_tag=tags,
#                                    content=content,
#                                    icon=icon)
#             return HttpResponseRedirect(reverse('article:index'))
#         else:
#             errors = form.errors
#             return render(request,'add_article.html',{'errors':errors})


def del_article(request):
    if request.method == 'POST':
        id = request.GET.get('id')
        Article.objects.filter(pk=id).delete()
        return JsonResponse({'code': 200, 'msg': 'success'})


def update_article(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        article = Article.objects.filter(pk=id).first()
        parts = Part.objects.all()
        return render(request, 'update_article.html', {'article': article, 'parts': parts})
    if request.method == 'POST':
        id = request.GET.get('id')
        title = request.POST.get('title')
        part = request.POST.get('part')
        tags = request.POST.get('tags')
        content = request.POST.get('content')
        icon = request.FILES.get('icon')
        if not all([title, content]):
            msg = '标题和内容必填'
            return render(request, 'add_article.html', {'msg': msg})
        # 更新文章
        Article.objects.filter(pk=id).update(a_title=title,
                                             a_part=part,
                                             a_tag=tags,
                                             content=content,
                                             icon=icon)

        return HttpResponseRedirect(reverse('article:index'))


def category(request):
    if request.method == 'GET':
        page = int(request.GET.get('page', 1))
        parts = Part.objects.all()
        count = len(parts)
        pg = Paginator(parts, 5)
        parts = pg.page(page)

        flag = 'part'
        return render(request, 'category.html', {'parts': parts,'count':count,'flag':flag})
    if request.method == 'POST':
        p_name = request.POST.get('name')
        p_alias = request.POST.get('alias')
        if not p_name:
            msg = '栏目必填,别名随意'
            return render(request, 'category.html', {'msg': msg})
        Part.objects.create(p_name=p_name,
                            p_alias=p_alias)
        return HttpResponseRedirect(reverse('article:category'))


def update_category(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        part = Part.objects.filter(pk=id)[0]
        return render(request, 'update_category.html', {'part': part})
    if request.method == 'POST':
        id = request.GET.get('id')
        p_name = request.POST.get('name')
        p_alias = request.POST.get('alias')
        if not p_name:
            msg = '栏目必填,别名随意'
            return render(request, 'category.html', {'msg': msg})
        Part.objects.filter(pk=id).update(p_name=p_name,
                                          p_alias=p_alias)
        return HttpResponseRedirect(reverse('article:category'))
