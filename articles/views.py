# touch articles/views.py
# articles/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Article
from .forms import ArticleForm
from django.http import JsonResponse
from django.core.paginator import Paginator


@login_required
def article_list(request):
    # 获取所有文章
    article_list = Article.objects.all()
    # 每页显示 10 篇文章
    page_size = request.GET.get('page_size', 3)
    paginator = Paginator(article_list, page_size)
    # 获取页码参数，默认为第 1 页
    page = request.GET.get('page', 1)
    # 获取当前页的文章列表
    articles = paginator.get_page(page)
    return render(request, 'articles/list.html', {'articles': articles})


@login_required
def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'articles/detail.html', {'article': article})


@login_required
def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            messages.success(request, '文章创建成功！')
            return redirect('articles:detail', pk=article.pk)
    else:
        form = ArticleForm()
    return render(request, 'articles/create.html', {'form': form})


def search_articles(request):
    if 'title' in request.GET:
        title = request.GET.get('title')
        articles = Article.objects.filter(title__icontains=title)
        articles_data = list(articles.values())
        return JsonResponse({'articles': articles_data})
    else:
        return JsonResponse({'error': '缺少标题参数'}, status=400)


