from django.urls import path

from . import views


app_name = 'gallery'
urlpatterns = [
    # 浏览图片
    path('', views.pics, name='pics'),

    # 上传图片
    path('recv_pic', views.recv_pic, name='recv_pic'),
    # 图片详情 scan
    path('scan/<int:number>', views.scan, name='scan')
]