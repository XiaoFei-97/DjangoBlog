# _*_ coding:utf-8 _*_

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),  # 访问地址:主机名+端口号/
    url(r'^detail/(?P<pk>\d+)$', views.detail, name='detail'),  # 访问地址:主机名+端口号/detail/pk
    url(r'^category/(?P<pk>\d+)$', views.category, name='category'),  # 访问地址:主机名+端口号/category/pk
    url(r'^blog', views.blog, name='blog'),  # 访问地址:主机名+端口号/blog
    url(r'^date/(\d+)/(\d+)', views.date, name='date'),  # 访问地址:主机名+端口号/date/年/月
    url(r'^category_list/', views.category_list, name='category_list'),
    url(r'^date_list/', views.date_list, name='date_list'),
]

handler404 = views.page_not_found
