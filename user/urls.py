from django.urls import path

from . import views


app_name = 'user'
urlpatterns = [
    path('captcha', views.get_captcha, name='captcha'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    # register
    path('register', views.register, name='register')
]