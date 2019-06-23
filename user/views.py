import random
from io import BytesIO

from PIL import ImageDraw, Image, ImageFont
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.contrib import auth

from .models import UserInfo
from .forms import UserModelForm

# Create your views here.


def login(request):
    if request.is_ajax():
        res = {'user': None, 'error_msg': ''}
        # 依次验证验证码 用户名/密码
        if request.POST.get('captcha').lower() == request.session.get('captcha_words').lower():
            user_obj = auth.authenticate(username=request.POST.get('user'), password=request.POST.get('pwd'))
            if user_obj:
                # 用户名/密码正确
                auth.login(request, user_obj)
                # 设置session
                request.session['username'] = user_obj.username
                request.session['is_login'] = True
                res['user'] = request.POST.get('user')
                return JsonResponse(res)
            else:
                res['error_msg'] = '用户名或密码有误'
                return JsonResponse(res)
        else:
            # 处理验证码失败
            res['error_msg'] = '验证码有误'
            return JsonResponse(res)


def logout(request):
    auth.logout(request)
    request.session['is_login'] = False
    return HttpResponse('成功登出')


def register(request):
    if request.is_ajax():
        form = UserModelForm(request.POST)
        res = {'is_reg': False}
        if form.is_valid():
            if not UserInfo.objects.filter(username=request.POST.get('username')):
                form.cleaned_data.pop('r_password')
                UserInfo.objects.create_user(**form.cleaned_data)
                res = {'is_reg': True}
                return JsonResponse(res)
            else:
                res['reg_err'] = '已存在同名用户'
                return JsonResponse(res)
        else:
            res = {'is_reg': False, 'reg_err': form.errors}
            return JsonResponse(res)


def get_captcha(request):
    img = Image.new('RGB', (200, 35), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    font = ImageFont.truetype(font='static/fonts/Rotonda-Bold.otf', size=20)
    captcha_words = ''

    for i in range(6):
        # 三次随机  数字/大小写英文 验证码
        cap_num = str(random.randint(0, 9))
        cap_upper_alp = chr(random.randint(65, 90))
        cap_lower_alp = chr(random.randint(97, 122))

        # img上依次写上6个char
        draw = ImageDraw.Draw(img)
        captcha_word = random.choice([cap_num, cap_lower_alp, cap_upper_alp])
        draw.text((20+i*20, 7), captcha_word, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), font=font)
        captcha_words += captcha_word

    # 将验证码 保存到session
    request.session['captcha_words'] = captcha_words

    f = BytesIO()
    img.save(f, 'png')
    data = f.getvalue()

    return HttpResponse(data)


def reg_collapse(request):
    # reg 信息
    reg_info = UserModelForm
    return reg_info