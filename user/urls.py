from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login/', views.login, name='login'),  # 访问地址:主机名+端口号/login
    url(r'^register/', views.register, name='register'),  # 访问地址:主机名+端口号/register
    url(r'^login_for_modal/', views.login_for_modal, name='login_for_modal'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^user_info/', views.user_info, name='user_info'),
    url(r'^about/', views.about, name='about'),
    url(r'^change_name/', views.change_name, name='change_name'),
    url(r'^change_password/', views.change_password, name='change_password'),
    url(r'^forgot_password/', views.forgot_password, name='forgot_password'),
    url(r'^bind_email/', views.bind_email, name='bind_email'),
    url(r'^send_verification_code/', views.send_verification_code, name='send_verification_code'),
]