from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [

    # 管理自己的文章
    path('manage', views.manage, name='manage'),

    # add article
    path('new', views.new, name='new'),

    # 文章详情
    path('detail/<int:number>', views.detail, name='detail'),

    # edit
    path('edit/<int:number>', views.edit, name='edit'),

    # search
    path('search/', views.search, name='search')

]
