from django import forms  # django表单功能
from django.contrib import auth
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    """
    用户登录表单
    """
    # 用户名
    username = forms.CharField(label='帐号',
                               widget=forms.TextInput(
                                   attrs={'placeholder': '请输入用户名'}))

    # 密码
    password = forms.CharField(label='密码',
                               widget=forms.PasswordInput(
                                   attrs={'placeholder': '请输入密码'}))

    def clean(self):
        """
        清洗输入不合格的表单
        :return: 清洗后的数据
        """
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = auth.authenticate(username=username, password=password)
        # 判断用户是否存在
        if user is None:
            raise forms.ValidationError('用户名或密码不正确,请重试')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data


class RegForm(forms.Form):
    """
    用户注册表单
    """
    # 用户名
    username = forms.CharField(label='账号',
                               max_length=30,
                               min_length=3,
                               widget=forms.TextInput(
                                   attrs={'placeholder': '请输入用户名'}))

    # 邮箱
    email = forms.EmailField(label='邮箱',
                             widget=forms.EmailInput(
                                   attrs={ 'placeholder': '请输入邮箱'}))

    # 密码
    password = forms.CharField(label='密码',
                               min_length=6,
                               widget=forms.PasswordInput(
                                   attrs={'placeholder': '请输入密码'}))

    # 再次输入密码
    password_again = forms.CharField(label='密码',
                                     min_length=6,
                                     widget=forms.PasswordInput(
                                        attrs={'placeholder': '再输入一次密码'}))

    def clean_username(self):
        """
        清洗输入的用户名
        :return: 清洗后的用户名
        """
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在')
        return username

    def clean_email(self):
        """
        清洗输入的邮箱
        :return: 清洗后的邮箱
        """
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已存在')
        return email

    def clean_password_again(self):
        """
        清洗第二次输入的密码
        :return: 输入一致的密码
        """
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']

        if password != password_again:
            raise forms.ValidationError('两次输入的密码不一致')
        return password


