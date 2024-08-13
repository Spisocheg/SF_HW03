from django.urls import path, include
from .views import *


url_news_current = [
    path('', PostNewsDetail.as_view(), name='news_detail'),
    path('edit/', PostNewsEdit.as_view(), name='news_edit'),
    path('delete/', PostNewsDelete.as_view(), name='news_delete'),
]

url_news = [
    path('', PostNewsList.as_view(), name='news_list'),
    path('create/', PostNewsCreate.as_view(), name='news_create'),
    path('<int:pk>/', include(url_news_current)),
]


url_articles_current = [
    path('', PostArticlesDetail.as_view(), name='article_detail'),
    path('edit/', PostArticlesEdit.as_view(), name='article_edit'),
    path('delete/', PostArticlesDelete.as_view(), name='article_delete'),
]

url_articles = [
    path('', PostArticlesList.as_view(), name='article_list'),
    path('create/', PostArticlesCreate.as_view(), name='article_create'),
    path('<int:pk>/', include(url_articles_current)),
]


urlpatterns = [
    path('', PostsList.as_view(), name='posts_list'),
    path('search/', PostsSearch.as_view(), name='search'),
    path('news/', include(url_news)),
    path('articles/', include(url_articles)),
]
