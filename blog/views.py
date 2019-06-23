from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import auth
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Avg, Max
from django.http import JsonResponse
from django.db.models import F, Q

from .models import Articles, UserInfo
from .forms import ArticleModelForm
from user.forms import UserModelForm
from user.views import reg_collapse


# Create your views here.


def decorate_logo(f):
    def inner(request, *args, **kwargs):
        res = {}
        if request.session.get('is_login'):
            username = request.session.get('username')
            res['username'] = username
        ret = f(request, *args, **kwargs)
        return ret

    return inner


def index(request, by_month=None, classify=None):

    # 进行归档 分类 或显示全部  (is_delete=0)
    if by_month:
        blogs = Articles.objects.filter(write_time__month=by_month, is_delete=0, is_public=1).order_by('-write_time')
    elif classify:
        blogs = Articles.objects.filter(is_delete=0, is_public=1, type_id=classify).order_by('-write_time')
    else:
        blogs = Articles.objects.filter(Q(is_delete=0) & Q(is_public=1)).order_by('-write_time')

    res = {'blogs': blogs, 'username': ''}
    # reg 信息
    reg_info = UserModelForm
    res['reg_info'] = reg_info

    pagination_blog(request, blogs, res, perpage=3)
    # 登录
    if request.session.get('is_login'):
        username = request.session.get('username')
        res['username'] = username
    # res['pageRange'] = pageRange
    # res['blogs'] = blogs

    # 右侧 最新/归档/分类
    res = body_right(res)
    return render(request, 'blog/index.html', res)


def detail(request, number):
    """ 文章详情 """
    res = {}
    blog_obj = Articles.objects.filter(pk=number).first()
    res['blog'] = blog_obj
    # reg 信息
    reg_info = UserModelForm
    res['reg_info'] = reg_info
    if request.session.get('is_login'):
        username = request.session.get('username')
        res['username'] = username
        return render(request, 'blog/detail.html', res)

    return render(request, 'blog/detail.html', res)


def manage(request):
    """管理界面"""
    res = {}
    if request.method == 'GET':
        username = request.session.get('username')
        res['username'] = username
        form = ArticleModelForm()
        res['form'] = form
        blogs = Articles.objects.filter(author=UserInfo.objects.filter(username=username).first(),
                                        is_delete=0).order_by('-write_time')
        res['blogs'] = blogs

        return render(request, 'blog/manage.html', res)
    elif request.is_ajax():
        print(request.POST)
        Articles.objects.filter(pk=request.POST.get('pk')).update(is_delete=1)
        res['is_deleted'] = True
        return JsonResponse(res)


def new(request):
    """新增"""
    username = request.session.get('username')
    if request.method == 'GET':
        form = ArticleModelForm()
        return render(request, 'blog/new.html', {'username': username, 'form': form})
    elif request.method == 'POST':
        form = ArticleModelForm(request.POST)
        if form.is_valid():
            Articles.objects.create(author=UserInfo.objects.filter(username=username).first(),
                                    write_time=timezone.now(),
                                    **form.cleaned_data)
            return redirect('index')
        else:
            """不能成功上传"""
            form = ArticleModelForm(request.POST)
            return render(request, 'blog/new.html', {'username': username, 'form': form})


def edit(request, number):
    res = {}
    username = request.session.get('username')
    res['username'] = username
    blogs = Articles.objects.filter(pk=number)
    blog_obj = blogs.first()
    if request.method == 'GET':
        form = ArticleModelForm(instance=blog_obj)
        res['form'] = form
        return render(request, 'blog/edit.html', res)
    elif request.method == 'POST':
        form = ArticleModelForm(request.POST, blog_obj)
        if form.is_valid():
            blogs.update(author=UserInfo.objects.filter(username=username).first(), write_time=timezone.now(),
                         **form.cleaned_data)
            return redirect('blog:manage')


def search(request):
    res = {}
    blogs = Articles.objects.all()
    search_content = request.GET.get('search-content', '')
    if search_content:
        res['search_content'] = search_content
        blogs = Articles.objects.filter(
            Q(is_delete=0) & Q(is_public=1) & Q(title__icontains=res['search_content'])).order_by('-write_time')
    # 右侧 最新/归档/分类
    res = body_right(res)
    # 登录改变logo
    res = change_logo(request, res)
    # 分页
    res = pagination_blog(request, blogs, res, perpage=2)

    return render(request, 'blog/index.html', res)


def body_right(res):
    # 最新文章  5篇
    new_blogs = Articles.objects.filter(is_delete=0).order_by('-write_time')
    res['new_blogs'] = new_blogs[:5]

    # 时间归档
    by_month = Articles.objects.filter(is_delete=0, is_public=1).values('write_time__year',
                                                                        'write_time__month').annotate(
        Count('pk')).order_by('-write_time__year', '-write_time__month')
    res['by_month'] = by_month

    # 分类
    classify_all = Articles.objects.filter(Q(is_delete=0) & Q(is_public=1)).count()
    classify = Articles.objects.filter(Q(is_delete=0) & Q(is_public=1)).values('type__name', 'type_id').annotate(
        Count('pk')).order_by('-pk__count')
    res['classify_all'] = classify_all
    res['classify'] = classify

    return res


def change_logo(request, res):
    if request.session.get('is_login'):
        username = request.session.get('username')
        res['username'] = username
    return res


def pagination_blog(request, blogs, res, perpage):
    paginator = Paginator(blogs, perpage)
    page = request.GET.get('page')
    # url上无页码信息.
    if not page:
        page = '1'

    currentPage = int(page)
    #  如果页数十分多时，换另外一种显示方式
    if paginator.num_pages > 11:

        if currentPage - 5 < 1:
            pageRange = range(1, 11)
        elif currentPage + 5 > paginator.num_pages:
            pageRange = range(currentPage - 5, paginator.num_pages + 1)

        else:
            pageRange = range(currentPage - 5, currentPage + 5)

    else:
        pageRange = paginator.page_range
    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        blogs = paginator.page(1)
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages)

    res['pageRange'] = pageRange
    res['blogs'] = blogs

    return res
