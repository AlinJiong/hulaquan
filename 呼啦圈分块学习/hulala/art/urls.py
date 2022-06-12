from django.urls import re_path, path

from . import views

urlpatterns = [
    re_path(r'^article/$', views.ArticleView.as_view()),
    re_path(r'^article/(?P<pk>\d+)/$', views.ArticleView.as_view()),
    re_path(r'^comment/$', views.CommentView.as_view()),
    re_path(r'^comment/(?P<pk>\d+)/$', views.CommentView.as_view()),
    re_path(r'^new/comment/$', views.NewCommentView.as_view()),
    path('login/', views.Login.as_view()),
    path('new/edit/', views.NewEdit.as_view()),
]
