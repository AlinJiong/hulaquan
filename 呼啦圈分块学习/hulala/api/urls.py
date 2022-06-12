from django.urls import re_path, path

from . import views
from .views import CategoryView

urlpatterns = [
    re_path(r'^category/$', CategoryView.as_view()),
    re_path(r'^category/(?P<pk>\d+)/$', CategoryView.as_view()),
    re_path(
        r'^tag/$', views.TagView.as_view({'get': 'list', 'post': 'create'})),
    re_path(r'^tag/(?P<pk>\d+)/$',
            views.TagView.as_view({'get': 'retrieve', 'post': 'create', 'delete': 'destroy', 'put': 'update',
                                   'patch': 'partial_update'})),
    re_path(r'^article/$', views.Article.as_view()),
    re_path(r'^article/(?P<pk>\d+)/$', views.Article.as_view()),
    path('page/article/', views.PageArticle.as_view()),
]
