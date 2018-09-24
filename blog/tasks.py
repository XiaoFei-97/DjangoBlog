from __future__ import absolute_import
from celery import shared_task
from django.core.cache import cache  # 缓存数据
# from blog.models import *
# from django.contrib.contenttypes.models import ContentType
# from django.db.models import Q
from read_statistics.utils import *


@shared_task
def get_post_list():
    post_list = Post.objects.filter(Q(display=0) | Q(display__isnull=True))
    # 30*60表示30秒*60,也就是半小时
    cache.set('post_list', post_list, 30 * 60)


@shared_task
def get_new_publish():
    new_publish = Post.objects.filter(Q(display=0) | Q(display__isnull=True))[:15]
    # 60*60表示60秒*60,也就是1小时
    cache.set('new_publish', new_publish, 30 * 60)


@shared_task
def get_new_recommend():
    post_content_type = ContentType.objects.get_for_model(Post)
    new_recommend = get_new_recommend_post(post_content_type)
    # 60*60表示60秒*60,也就是1小时
    cache.set('new_recommend', new_recommend, 30 * 60)


@shared_task
def get_last_7_days_hot_data():
    last_7_days_hot_data = get_7_days_read_posts()
    # 60*60表示60秒*60,也就是1小时
    cache.set('last_7_days_hot_data', last_7_days_hot_data, 30 * 60)


@shared_task
def get_last_30_days_hot_data():
    last_30_days_hot_data = get_30_days_read_posts()
    # 60*60表示60秒*60,也就是1小时
    cache.set('last_30_days_hot_data', last_30_days_hot_data, 30 * 60)


@shared_task
def get_all_hot_posts():
    all_hot_posts = get_all_read_posts()
    # 60*60表示60秒*60,也就是1小时
    cache.set('all_hot_posts', all_hot_posts, 30 * 60)


@shared_task
def get_post_dates():
    post_dates = Post.objects.dates('created_time', 'month', order='DESC')
    # 60*60表示60秒*60,也就是1小时
    cache.set('post_dates', post_dates, 30 * 60)