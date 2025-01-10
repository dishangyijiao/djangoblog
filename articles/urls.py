# touch articles/urls.py
# articles/urls.py
from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('', views.article_list, name='list'),
    path('create/', views.article_create, name='create'),
    path('<int:pk>/', views.article_detail, name='detail'),
    path('search/', views.search_articles, name='search_articles'),
]
