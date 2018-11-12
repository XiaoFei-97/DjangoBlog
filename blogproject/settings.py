"""
Django settings for blogproject project.

Generated by 'django-admin startproject' using Django 1.10.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# django celery 配置
import djcelery

djcelery.setup_loader()
# BROKER_URL = 'django://'  # 开发环境
BROKER_URL = 'redis://localhost:6379/1'  # 生产环境
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'  # 定时任务
# CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Shanghai'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'unn!knl%n46(^9q1ody(n+5=m2r693nek7aabd_7v%l+820_lq'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'xadmin',
    'djcelery',  # celery
    # 'djkombu',
    'kombu.transport.django',
    'django_redis',
    'crispy_forms',
    'ckeditor',  # 富文本编辑器
    'ckeditor_uploader',
    'DjangoUeditor',
    'haystack',
    'blog',
    'read_statistics',
    'comment',
    'likes',
    'user',
    'oauth',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'blogproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'blogproject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'blog',
        'USER': os.environ.get('DJANGO_MYSQL_USER'),
        'PASSWORD': os.environ.get('DJANGO_MYSQL_PASSWORD'),
        'HOST': os.environ.get('DJANGO_MYSQL_HOST'),
        'PORT': '3306'
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

# 配置静态文件路径,静态文件包括css,js,image
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static/')
]
# nginx
STATIC_ROOT = '/home/jzf/sites/jzfblog.com/static/'

CKEDITOR_JQUERY_URL = 'https://apps.bdimg.com/libs/jquery/2.1.4/jquery.min.js'

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# 配置ckeditor
CKEDITOR_UPLOAD_PATH = 'uploads/'

CKEDITOR_IMAGE_BACKEND = 'PIL'

# 自定义参数
EACH_RAGE_BLOG_NUMBER = 10


CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': (
            ['div', 'Source', '-', 'Save', 'NewPage', 'Preview', '-', 'Templates'],
            ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Print', 'SpellChecker', 'Scayt'],
            ['Undo', 'Redo', '-', 'Find', 'Replace', '-', 'SelectAll', 'RemoveFormat', 'CodeSnippet'],
            ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton', 'HiddenField'],
            ['Bold', 'Italic', 'Underline', 'Strike', '-', 'Subscript', 'Superscript'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', 'Blockquote'],
            ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink', 'Anchor'],
            ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'codesnippet'],
            ['Styles', 'Format', 'Font', 'FontSize'],
            ['TextColor', 'BGColor'],
            ['Maximize', 'ShowBlocks', '-', 'About', 'pbckcode'],
        ),
        # 插件
        'extraPlugins': ','.join(['codesnippet','uploadimage','widget','lineutils',]),
    },

    'comment_ckeditor': {
        'toolbar': 'custom',
        'toolbar_custom': [
            ['Bold', 'Italic', 'Underline', 'Strike', '-', 'Subscript', 'Superscript'],
            ['TextColor', 'BGColor', 'RemoveFormat'],
            ['NumberedList', 'BulletedList'],
            ['Link', 'Unlink'],
            ['Smiley', 'SpecialChar', 'Blockquote'],
        ],
        'width': 'auto',
        'height': '180',
        'tabSpaces': 4,
        'removePlugins': 'elementspath',
        'resize_enabled': False,
    }
}

# 缓存设置
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': '127.0.0.1:6379',
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },
}

HAYSTACK_CONNECTIONS = {
    'default': {
        # 使用whoosh引擎
        'ENGINE': 'haystack.backends.whoosh_cn_backend.WhooshEngine',
        # 索引文件路径
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
    }
}

# 自动生成索引
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 10

# 发送邮件设置
# https://doc.djangoproject.com/en/2.0/ref/settings/#email
# https://doc.djangoproject.com/en/2.0/topics/email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = '652380120@qq.com'
EMAIL_HOST_PASSWORD = 'ygrwfejppgoxbfac'  # 授权码
EMAIL_SUBJECT_PREFIX = '[蒋振飞的博客] '
EMAIL_USE_TLS = True  # 与SMTP服务器通信时，是否启动TLS链接(安全链接)

# github登录
GITHUB_APP_ID = '50675d10fab22eba7342'
GITHUB_KEY = 'af39cde883162c12ce57e69cb078708aba915ccd'
GITHUB_CALLBACK_URL = 'https://jzfblog.com/oauth/github_check'  # 填写你的回调地址

# QQ登录
QQ_APP_ID = '************'
QQ_KEY = '*******************8'
QQ_CALLBACK_URL = 'http://127.0.0.1:8000/oauth/qq_check'    # 填写你的回调地址

# 新浪微博登录
WEIBO_APP_ID = '************'
WEIBO_KEY = '*****************'
WEIBO_CALLBACK_URL = 'http://127.0.0.1:8000/oauth/weibo_check'    # 填写你的回调地址



