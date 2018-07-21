from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login/', views.login, name='login'),  # 访问地址:主机名+端口号/login
    url(r'^register/', views.register, name='register'),  # 访问地址:主机名+端口号/register
    url(r'^login_for_modal/', views.login_for_modal, name='login_for_modal'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^user_info/', views.user_info, name='user_info'),
    url(r'^about/', views.about, name='about'),

]