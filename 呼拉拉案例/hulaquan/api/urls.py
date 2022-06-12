from django.urls import path, re_path

from .views import account
from .views import order, comment, article

urlpatterns = [
    re_path(r'login/$', account.LoginView.as_view()),
    path('order/', order.OrderView.as_view()),
    path('comment/', comment.CommentView.as_view()),
    re_path(r'^comment/(?P<pk>\d+)/$', comment.CommentView.as_view()),
    path('article/', article.ArticleView.as_view()),
    re_path(r'^article/(?P<pk>\d+)/$', article.ArticleDetailView.as_view()),
    # path('article/', article.ArticleView.as_view({'get': 'list', 'post': 'create'})),
    # re_path(r'^article/(?P<pk>\d+)/$', article.ArticleView.as_view({'get': 'retrieve'})),

]
