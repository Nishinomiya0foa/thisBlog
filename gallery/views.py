from django.shortcuts import render, HttpResponse
from django.utils import timezone
from django.http import JsonResponse

from .models import Pic
from .forms import PicModelForm
from user.models import UserInfo
from user.forms import UserModelForm
# Create your views here.


def pics(request):
    """画廊总览"""
    res = {}
    form = PicModelForm()
    res['forms'] = form

    # reg 信息
    reg_info = UserModelForm
    res['reg_info'] = reg_info
    if request.session.get('is_login'):
        username = request.session.get('username')
        res['username'] = username
        is_superuser = UserInfo.objects.filter(username=request.session.get('username')).first().is_superuser
        res['is_superuser'] = is_superuser

    imgs = Pic.objects.all().order_by('-write_time')
    res['imgs'] = imgs
    return render(request, 'pics/pics.html', res)


def recv_pic(request):
    """上传图片"""
    try:
        is_super = UserInfo.objects.filter(username=request.session.get('username')).first().is_superuser
    except:
        return HttpResponse('未登录')
    if is_super == 1:
        """当前用户为superuser"""
        if request.method == 'GET':
            res = {}
            form = PicModelForm()
            res['forms'] = form
            return render(request, 'pics/upload.html', res)
        elif request.method == 'POST':
            res = {}
            print(request.session.get('username'))
            form = PicModelForm(request.POST, request.FILES)
            if form.is_valid():
                print(form.cleaned_data)
                Pic.objects.create(author=UserInfo.objects.filter(username=request.session.get('username')).first(), write_time=timezone.now(), **form.cleaned_data)
                return HttpResponse('OK')
            else:
                print(form.errors)
                res['forms'] = PicModelForm(request.POST, request.FILES)
                return render(request, 'pics/upload.html', res)
    else:
        print('不ok')

    # if request.session.get('username'):
    #     if UserInfo.objects.filter(username=request.session.get('username')).first().is_superuser == 1:
    #         print(UserInfo.objects.filter(username=request.session.get('username')))
    #         if request.method == 'GET':
    #             res = {}
    #             form = PicModelForm()
    #             res['forms'] = form
    #             return render(request, 'pics/upload.html', res)
    #         elif request.method == 'POST':
    #             res = {}
    #             print(request.session.get('username'))
    #             form = PicModelForm(request.POST, request.FILES)
    #             if form.is_valid():
    #                 print(form.cleaned_data)
    #                 form.save()
    #                 return HttpResponse('OK')
    #             else:
    #                 print(form.errors)
    #                 res['forms'] = PicModelForm(request.POST, request.FILES)
    #                 return render(request, 'pics/upload.html', res)
    #         else:
    #             return HttpResponse('您未登录或没有此权限')
    #     else:
    #         print(UserInfo.objects.filter(username=request.session.get('username')).first().is_superuser)


def scan(request, number):
    res = {}
    pic_obj = Pic.objects.filter(pk=number).first()
    res['pic_obj'] = pic_obj
    # 传递前一个/后一个
    pic_obj_next = Pic.objects.filter(pk__lt=number).first()  # prev/left
    pic_obj_prev = Pic.objects.filter(pk__gt=number).first()  # next / right
    res['pic_obj_prev'] = pic_obj_prev
    res['pic_obj_next'] = pic_obj_next
    if request.is_ajax():
        print(pic_obj_prev, pic_obj_next)
        return JsonResponse(res)

    return render(request, 'pics/detail.html', res)