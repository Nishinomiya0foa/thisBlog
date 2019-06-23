import re
import time

from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import reverse, HttpResponse, Http404

from blog.models import Articles


class UpdateLogo(MiddlewareMixin):
    """用户已登录则更改Logo"""
    pass


class LoginOrNot(MiddlewareMixin):
    def process_request(self, request):
        # 登录验证
        # detail_pg = re.findall('detail/(\d+)',request.META.get('PATH_INFO'))
        edit_pg = re.findall('edit/(\d+)', request.META.get('PATH_INFO'))
        check_url = [reverse('blog:manage'), reverse('blog:new'), reverse('gallery:recv_pic')]
        if edit_pg or request.path in check_url:
            if not request.user.is_authenticated:
                # return HttpResponse('<h1>请登录哦~</h1><a class="btn btn-default" href="/">返回首页</a>')
                raise Http404('登录可访问')


class Update_views(MiddlewareMixin):
    """文章阅读次数"""
    def process_request(self, request):
        detail_obj = re.search('/detail/', request.META.get('PATH_INFO'))
        # 没有访问过  或   访问间隔大于 10
        if detail_obj:
            pk_obj = re.findall('detail/(.*)?', request.META.get('PATH_INFO'))
            if pk_obj:
                article_obj = Articles.objects.filter(pk=pk_obj[0])
                if request.session.get('view_blog') != pk_obj[0] or \
                        request.session.get('view_blog') == pk_obj[0] and\
                        time.time() - request.session['last_view'] > 300:
                    if article_obj:
                        v = article_obj.first().views + 1
                        article_obj.update(views=v)
                        # request.session['is_new_in_3_min'] = False
                        request.session['view_blog'] = pk_obj[0]
                        request.session['last_view'] = time.time()






