"""myblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from blog import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # index
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('index/record/<int:by_month>', views.index, name='index_record'),
    path('index/classify/<int:classify>', views.index, name='index_classify'),
    path('index/record/<int:by_month>/classify/<int:classify>', views.index, name='index'),

    # user
    path('user/', include('user.urls')),

    # blog
    path('blog/', include('blog.urls')),

    # gallery
    path('gallery/', include('gallery.urls')),

    # 富文本
    path('ckeditor/', include('ckeditor_uploader.urls'))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
